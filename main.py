import streamlit as st
from utils import generate_script
import os

st.title('🔥短视频脚本生成器')
st.write('注：维基百科搭载，需科学上网')

with st.sidebar:
    input_api_key = st.text_input('请输入密钥(已部署环境变量启用环境变量即可):', type = 'password')
    base_url = st.text_input('请输入镜像网站地址(可选)：')
    st.markdown('[获取OPENAI api密钥](https://platform.openai.com/api-keys)')

    # 初始化状态
    if "enabled" not in st.session_state:
        st.session_state.enabled = False

    # 显示当前状态
    status = "✅ 已启用" if st.session_state.enabled else "❌ 已禁用"
    st.markdown(f"环境变量部署：{status}")

    # 设置按钮文字和颜色
    button_label = "🔴 禁用" if st.session_state.enabled else "🟢 启用"

    # 注意：Streamlit 默认不支持颜色按钮，所以我们用 markdown 或第三方控件美化
    if st.button(button_label):
        st.session_state.enabled = not st.session_state.enabled

    side_submit = st.session_state.enabled

    if side_submit:
        open_api_key = os.getenv('OPENAI_API_KEY')
    if not side_submit:
        open_api_key = input_api_key
        
subject = st.text_input('请输入视频主题：')
video_length = st.number_input('请输入视频大致时长(min)：', min_value = 0.1, step = 0.1)
creativity = st.slider('请输入视频脚本的创造力(数字小则严谨，数字大则更多样)：', min_value = 0.0 , max_value= 1.0 ,value = 0.2 , step = 0.1)
submit = st.button('生成脚本')

if submit and not openai_api_key:
    st.info('请输入OpenAI密钥')
    st.stop()
if submit and not subject:
    st.info('请输入主题')
    st.stop()

if submit:
    with st.spinner('AI思考中，请稍等…'):
        if openai_api_key:
            if base_url:
                search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key, base_url)
            else:
                search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
        st.success('视频脚本已生成！')
        st.subheader('标题：')
        st.write(title)
        st.subheader('视频脚本：')
        st.write(script)
        with st.expander('维基百科搜索结果：'):
            st.info(search_result)
