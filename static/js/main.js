document.addEventListener('DOMContentLoaded', function () {
  // Sidebar toggle for mobile
  const toggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Auto-dismiss alerts
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4500);
  });

  // Highlight active nav
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.getAttribute('href') === currentPath) {
      item.classList.add('active');
    }
  });

  const landingHeader = document.querySelector('.landing-header');
  if (landingHeader) {
    const toggleLandingHeader = () => {
      landingHeader.classList.toggle('is-hidden', window.scrollY > 40);
    };

    toggleLandingHeader();
    window.addEventListener('scroll', toggleLandingHeader, { passive: true });
  }

});
