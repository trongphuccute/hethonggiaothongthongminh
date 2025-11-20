document.getElementById('signupForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Ngăn reload trang

  const first = document.getElementById('firstName').value.trim();
  const email = document.getElementById('email').value.trim();

  if (first && email) {
    alert(`✅ Chào mừng ${first}! Bạn đã đăng ký thành công.`);
    // Có thể chuyển sang trang đăng nhập:
    window.location.href = "login.html";
  } else {
    alert("⚠️ Vui lòng điền đầy đủ thông tin!");
  }
});
