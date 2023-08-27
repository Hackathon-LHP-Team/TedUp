import streamlit as st

# import modules
from chat_setup_configuration import page_configure
from css_customization import customization
from page_management import management


# set up page configuration
page_configure()
customization()

# flask database
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathon_round_3_LHP_team" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------- Database -----------
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    user_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    Q_value_get = db.relationship('Q_values', backref='user')
    S_value_get = db.relationship('S_values', backref='user')
    chat_session_get = db.relationship('Chat_sessions', backref='user')
    
    
    @property
    def password():
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Chat_sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String, nullable=False)
    chat_message = db.relationship('Chat_messages', backref='chat_session')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Chat_messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    

class Q_values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class S_values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
# signup form
# with st.form(key='form_signup'):
#     st.write('Create an account')
#     form_name = st.text_input('name')
#     form_email = st.text_input('email')
#     form_user_name = st.text_input('user name')
#     form_password = st.text_input('password')
#     form_password_re = st.text_input('confirm password')
#     submit_button = st.form_submit_button(label='Submit')
    
#     if submit_button:
#         with app.app_context():
#             user = Users.query.filter_by(email=form_email).first()
#             if user is None:
#                 user = Users(name=form_name, email=form_email, user_name=form_user_name, password_hash=form_password)
#                 if form_password == form_password_re:
#                     db.session.add(user)
#                     db.session.commit()
                
# form
with st.form(key='form_login'):
    st.write('**LOGIN FORM**')
    form_email = st.text_input('email')
    form_password = st.text_input('password') 
    
    with st.expander("**Điều Khoản**"):
        st.markdown("""
            Điều khoản sử dụng dịch vụ theo dõi sức khoẻ
            Khi bạn chấp thuận và sử dụng dịch vụ theo dõi sức khoẻ của chúng tôi, bạn đồng ý với các điều khoản và điều kiện sau đây:
            \n- Bạn cho phép chúng tôi truy cập, thu thập, lưu trữ và xử lý các thông tin cá nhân và sức khoẻ của bạn ở mức cần thiết để cung cấp cho bạn các dịch vụ và tính năng liên quan đến việc theo dõi sức khoẻ của bạn, bao gồm  các thông tin phân tích, đồ thị miêu tả cảm xúc và các chỉ số khác. Đây là thông tin giúp chúng tôi có thể cung cấp cho bạn một dịch vụ toàn diện và cá nhân hoá.
            \n- Bạn cho phép chúng tôi sử dụng các thông tin cá nhân và sức khoẻ của bạn để phân tích, đánh giá và đưa ra các gợi ý, khuyến nghị và cảnh báo về tình trạng sức khoẻ của bạn, cũng như để liên lạc với bạn qua các kênh như email, tin nhắn, điện thoại hoặc các phương tiện khác khi cần thiết.
            \n- Bạn cho phép chúng tôi chia sẻ các thông tin cá nhân và sức khoẻ của bạn với các bên thứ ba có liên quan khi có yêu cầu của bạn hoặc khi có sự cho phép của bạn, hoặc khi có nhu cầu pháp lý hoặc y tế khẩn cấp. Các bên thứ ba có liên quan. Chúng tôi sẽ không thực hiện hành động này nếu không có sự cho phép của bạn.
            \n- Bạn hiểu rằng chúng tôi cam kết bảo mật và bảo vệ các thông tin cá nhân và sức khoẻ của bạn theo quy định của pháp luật và theo chính sách bảo mật của chúng tôi. Chúng tôi sẽ không tiết lộ, bán, cho thuê hoặc chuyển nhượng các thông tin cá nhân và sức khoẻ của bạn cho bất kỳ ai mà không có sự đồng ý của bạn, trừ khi có quyền hoặc nghĩa vụ pháp lý hoặc y tế để làm như vậy.
            \n- Bạn hiểu rằng việc sử dụng dịch vụ theo dõi sức khoẻ của chúng tôi không thay thế cho việc khám bệnh, chẩn đoán hoặc điều trị bởi các chuyên gia y tế. Bạn nên luôn tuân theo các hướng dẫn và lời khuyên của bác sĩ hoặc nhân viên y tế khi có liên quan đến sức khoẻ của bạn. Bạn không nên bỏ qua hoặc trì hoãn việc tìm kiếm sự giúp đỡ y tế khi cần thiết.
            \n- Bạn hiểu rằng việc sử dụng dịch vụ theo dõi sức khoẻ của chúng tôi có thể gặp phải các rủi ro, sai sót, lỗi hoặc sự cố kỹ thuật, và bạn chịu hoàn toàn trách nhiệm và rủi ro cho việc sử dụng dịch vụ của bạn. Chúng tôi không chịu trách nhiệm hoặc bồi thường cho bất kỳ thiệt hại, tổn thất, khiếu nại hoặc yêu cầu nào phát sinh từ việc sử dụng dịch vụ của bạn, trừ khi có quy định khác bằng văn bản.
            \n- Bạn có thể từ chối cho phép truy cập thông tin của bạn, nhưng điều đó có thể ảnh hưởng đến chất lượng và hiệu quả của dịch vụ theo dõi sức khoẻ của chúng tôi. Bạn có thể thay đổi cài đặt quyền riêng tư của bạn trong phần cài đặt tài khoản, hoặc liên hệ với chúng tôi để yêu cầu xóa hoặc sửa đổi các thông tin của bạn. Chúng tôi luôn tôn trọng quyền riêng tư và sự lựa chọn của bạn.
            \n Nếu bạn có bất kỳ câu hỏi, ý kiến hoặc phản hồi nào về điều khoản sử dụng dịch vụ theo dõi sức khoẻ của chúng tôi, xin vui lòng liên hệ với chúng tôi qua email: healthtracker@gmail.com. Xin cảm ơn bạn đã sử dụng dịch vụ của chúng tôi.
        """)
        agree  = st.checkbox('Tôi đồng ý')
    
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        with app.app_context():
            user = Users.query.filter_by(email=form_email).first()
            if agree and form_password == user.password_hash:
                st.success("successully login")
                
                
            
# with app.app_context():
#     user = Users.query.get_or_404(1)
    
# Chat session form
# with st.form(key='form_chat_session'):
#     st.write('New Chat session')
#     form_content = st.text_input('content')
#     submit_button = st.form_submit_button(label='Submit')
    
#     if submit_button:
#         with app.app_context():
#             user = Users.query.get_or_404(1)
#             chat_session = Chat_sessions(content=form_content, user_id=user.id)
#             db.session.add(chat_session)               
#             db.session.commit()
            
# # Chat message form
# with st.form(key='form_chat_message'):
#     st.write('New Chat message')
#     form_session_id = st.text_input('chat session id')
#     form_content = st.text_input('content message')
#     submit_button = st.form_submit_button(label='Submit')
    
#     if submit_button:
#         with app.app_context():
#             chat_message = Chat_messages(content=form_content, session_id=form_session_id) 
#             db.session.add(chat_message)               
#             db.session.commit()
    
    
# with app.app_context():
#     all_sessions = Chat_sessions.query.order_by(Chat_sessions.date_posted)
#     for session in all_sessions:
#         st.write(session.content)
#         all_messages = Chat_messages.query.order_by(Chat_messages.date_posted)
#         for message in all_messages:
#             if message.session_id == session.id:
#                 st.write(message.content)