import streamlit as st
from models.content_generator import ContentGenerator
from utils.database import save_content
from utils.database import init_db
from models.image_generator import ImageGenerator
from models.seo_optimizer import SEOOptimizer
from utils.database import get_db, ContentRecord

init_db()

st.set_page_config(page_title="AI Content Generator", layout="wide")

st.title("🤖 AI Content Generator")

generator = ContentGenerator()
seo = SEOOptimizer()
image_gen = ImageGenerator() 

tab1, tab2, tab3 = st.tabs(["Blog Posts", "Social Media", "History"])

with tab1:
    topic = st.text_input("Enter topic:")
    length = st.selectbox("Length:", ["short", "medium", "long"])
    
    if st.button("Generate Blog Post"):
        with st.spinner("Generating..."):
            content = generator.generate_blog_post(topic, length)
            content = generator.generate_blog_post(topic, length)

            # SEO optimization
            seo_data = seo.optimize(topic, content)

            # Generate image (optional)
            try:
                image_bytes = image_gen.generate_image(topic)
                st.image(image_bytes, caption="Generated Image")
            except Exception as e:
                st.warning(f"Image generation failed: {e}")

            # Show content
            st.subheader("📄 Generated Content")
            st.write(content)

            # Show SEO
            st.subheader("🔍 SEO Optimization")
            st.write(f"Slug: {seo_data['slug']}")
            st.write(f"Meta Title: {seo_data['meta_title']}")
            st.write(f"Meta Description: {seo_data['meta_description']}")
            st.write(f"Keywords: {', '.join(seo_data['keywords'])}")

with tab2:
    topic = st.text_input("Enter topic for social media:")
    platform = st.selectbox("Platform:", ["twitter", "instagram", "linkedin"])
    
    if st.button("Generate Posts"):
        posts = generator.generate_social_posts(topic, platform)
        for i, post in enumerate(posts, 1):
            st.write(f"**Post {i}:**\n{post}")
            save_content(topic, platform, post)
with tab3:
    st.subheader("📜 Content History")

    db = next(get_db())
    records = db.query(ContentRecord).order_by(ContentRecord.id.desc()).all()

    if not records:
        st.info("No history found yet.")
    else:
        for record in records:
            st.markdown("---")
            st.write(f"**Title:** {record.title}")
            st.write(f"**Prompt:** {record.prompt}")
            st.write(f"**Content:** {record.content[:300]}...")

            if record.created_at:
                st.caption(f"Created at: {record.created_at}")