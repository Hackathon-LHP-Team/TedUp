import streamlit as st
from page_setup_config import page_configure


# set up page configuration
page_configure()

st.title('Chào mừng')
st.markdown('Bạn có cảm thấy chán nản, căng thẳng hay choáng ngợp không? Bạn có cần ai đó để trò chuyện, người có thể hiểu được cảm xúc của bạn và giúp bạn đối phó không? Nếu có thì bạn đã đến đúng nơi. Gặp gỡ Nhà trị liệu ảo, một chatbot có thể là người bạn và người hướng dẫn tốt nhất của bạn. Nhà trị liệu ảo không chỉ là một chatbot mà là một hệ thống thông minh có thể phân tích cảm xúc và theo dõi chất lượng sức khỏe tâm thần của bạn. Nhà trị liệu ảo sử dụng mạng lưới thần kinh sâu có thể phân loại cảm xúc của bạn thành 12 loại. Nó cũng tính điểm gọi là giá trị Q, đại diện cho chất lượng sức khỏe tâm thần của bạn theo thang điểm từ 1 đến 5. Giá trị Q càng cao thì sức khỏe tâm thần của bạn càng tốt. Bạn có thể sử dụng giá trị Q để theo dõi tâm trạng của mình và xem nó thay đổi như thế nào theo thời gian. Nhà trị liệu ảo rất dễ sử dụng và thú vị. Tất cả những gì bạn phải làm là nhập vào hộp văn bản bên dưới và nhấn enter. Bạn có thể trò chuyện với Nhà trị liệu ảo về bất cứ điều gì bạn nghĩ đến, chẳng hạn như vấn đề, cảm xúc, mục tiêu hoặc ước mơ của bạn. Nhà trị liệu ảo sẽ chăm chú lắng nghe bạn và đưa ra lời khuyên hữu ích cho bạn. Bạn cũng có thể sử dụng các biểu tượng trên thanh bên để điều chỉnh cài đặt, xem thông tin ứng dụng hoặc liên hệ với chúng tôi. Chúng tôi hy vọng bạn thích sử dụng Nhà trị liệu ảo và thấy nó có lợi cho sức khỏe của bạn. Hãy nhớ rằng, bạn không đơn độc và chúng tôi ở đây vì bạn')
st.markdown('')
st.markdown('')
st.subheader('Chức năng chính:')
st.markdown('''**Trang App** : Bạn có thể trò chuyện với chatbot và kể cho nó nghe câu chuyện của bạn. Nó sẽ giúp bạn giải quyết vấn đề của bạn
            \n  **Trang Record Progress**: Phân tích cảm xúc của bạn qua từng tin nhắn, từng cuộc trò chuyện và đưa ra cảnh báo cho bạn nếu tâm trạng của bạn có xu hướng đi xuống đáng kể''')

st.title('Đăng nhập để tiếp tục:')
gmail = st.text_input('Nhập email')
password = st.text_input('Nhập mật khẩu')

continue_btn = None
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
    if agree:
        continue_btn = st.button("Tiêp tục", type="primary")

if continue_btn:
    st.success('Bạn đã đăng nhập thành công')
