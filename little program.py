from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String(50), nullable=False)  # 周次
    content = db.Column(db.Text, nullable=False)    # 汇报内容
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return f"<Report {self.id}>"

# 主页面：显示所有汇报
@app.route('/')
def index():
    reports = Report.query.order_by(Report.date_created.desc()).all()
    return render_template('index.html', reports=reports)

# 添加新汇报
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        week = request.form['week']
        content = request.form['content']
        new_report = Report(week=week, content=content)
        try:
            db.session.add(new_report)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your report."
    return render_template('add.html')

# 删除汇报
@app.route('/delete/<int:id>')
def delete(id):
    report_to_delete = Report.query.get_or_404(id)
    try:
        db.session.delete(report_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the report."

# 启动应用
if __name__ == '__main__':
    # 确保数据库存在
    with app.app_context():
        db.create_all()
    app.run(debug=True)