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

