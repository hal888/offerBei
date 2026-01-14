<template>
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-column brand-column">
        <div class="footer-logo">
          <img src="/logo.webp" alt="Offer贝" class="logo-img" />
          <span class="logo-text">Offer贝-AI面试助手</span>
        </div>
        <p class="footer-desc">专业AI面试工具，助力求职者轻松拿到心仪Offer。</p>
      </div>

      <div class="footer-column link-column">
        <h3>产品</h3>
        <ul>
          <li><router-link to="/resume">简历优化</router-link></li>
          <li><router-link to="/question-bank">智能题库</router-link></li>
          <li><router-link to="/mock-interview">模拟面试</router-link></li>
        </ul>
      </div>

      <div class="footer-column link-column">
        <h3>资源</h3>
        <ul>
          <li><router-link to="/manual">使用教程</router-link></li>
          <li><router-link to="/faq">常见问题</router-link></li>
        </ul>
      </div>

      <div class="footer-column contact-column">
        <h3>联系我们</h3>
        <div class="qr-codes">
          <div class="qr-item">
            <img src="/studio_arcode.png" alt="微信客服" class="qr-img" />
            <span>微信客服</span>
          </div>
        </div>
        <p class="contact-tip">使用中遇到任何问题，请随时联系我们</p>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 Offer贝. 保留所有权利.</p>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background-color: #0f172a; /* Dark background matching the image */
  color: #94a3b8;
  padding: 60px 0 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.5fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-column h3 {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 20px;
}

.brand-column .footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo-text {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 700;
}

.footer-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  max-width: 300px;
}

.link-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.link-column ul li {
  margin-bottom: 12px;
}

.link-column a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s;
  font-size: 0.95rem;
}

.link-column a:hover {
  color: #ffffff;
}

.contact-column .qr-codes {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
}

.qr-placeholder {
  width: 80px;
  height: 80px;
  background-color: #ffffff;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0f172a;
  font-size: 0.8rem;
  font-weight: bold;
}

.qr-img {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  object-fit: cover;
}

.contact-tip {
  font-size: 0.85rem;
  margin-top: 10px;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 20px 0;
  border-top: 1px solid #1e293b;
  text-align: center;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 30px;
    text-align: center;
  }
  
  .brand-column .footer-logo {
    justify-content: center;
  }
  
  .footer-desc {
    margin: 0 auto;
  }
  
  .contact-column .qr-codes {
    justify-content: center;
  }
}
</style>
