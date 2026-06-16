document.addEventListener('DOMContentLoaded', function () {
  // Sidebar toggle for mobile
  const toggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const sidebarResizer = document.getElementById('sidebarResizer');
  if (toggle && sidebar) {
    const isMobileLayout = () => window.matchMedia('(max-width: 992px)').matches;
    const minSidebarWidth = 180;
    const maxSidebarWidth = 360;
    const defaultSidebarWidth = 260;
    const setSidebarWidth = (width) => {
      const clampedWidth = Math.min(maxSidebarWidth, Math.max(minSidebarWidth, width));
      document.body.style.setProperty('--sidebar-resized-w', `${clampedWidth}px`);
      document.body.classList.add('sidebar-resized');
      localStorage.setItem('sidebarWidth', String(clampedWidth));
    };
    const applyStoredSidebarState = () => {
      const storedWidth = Number(localStorage.getItem('sidebarWidth'));
      if (!isMobileLayout() && storedWidth) {
        setSidebarWidth(storedWidth);
      }
      if (!isMobileLayout() && localStorage.getItem('sidebarCollapsed') === 'true') {
        document.body.classList.add('sidebar-collapsed');
      }
    };

    applyStoredSidebarState();

    toggle.addEventListener('click', () => {
      if (isMobileLayout()) {
        sidebar.classList.toggle('open');
        return;
      }

      document.body.classList.toggle('sidebar-collapsed');
      localStorage.setItem('sidebarCollapsed', document.body.classList.contains('sidebar-collapsed'));
    });

    document.addEventListener('click', (e) => {
      if (isMobileLayout() && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });

    window.addEventListener('resize', () => {
      sidebar.classList.remove('open');
      if (isMobileLayout()) {
        document.body.classList.remove('sidebar-collapsed');
      } else {
        applyStoredSidebarState();
      }
    });

    if (sidebarResizer) {
      sidebarResizer.addEventListener('pointerdown', (event) => {
        if (isMobileLayout() || document.body.classList.contains('sidebar-collapsed')) {
          return;
        }

        event.preventDefault();
        sidebarResizer.setPointerCapture(event.pointerId);
        document.body.classList.add('sidebar-resizing');
      });

      sidebarResizer.addEventListener('pointermove', (event) => {
        if (!document.body.classList.contains('sidebar-resizing')) {
          return;
        }

        setSidebarWidth(event.clientX);
      });

      const stopSidebarResize = (event) => {
        if (!document.body.classList.contains('sidebar-resizing')) {
          return;
        }

        document.body.classList.remove('sidebar-resizing');
        if (sidebarResizer.hasPointerCapture(event.pointerId)) {
          sidebarResizer.releasePointerCapture(event.pointerId);
        }
      };

      sidebarResizer.addEventListener('pointerup', stopSidebarResize);
      sidebarResizer.addEventListener('pointercancel', stopSidebarResize);
      sidebarResizer.addEventListener('dblclick', () => {
        setSidebarWidth(defaultSidebarWidth);
      });
    }
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
    let isPointerNearTop = false;
    const revealZoneHeight = 56;

    const toggleLandingHeader = () => {
      const shouldHide = window.scrollY > 40 && !isPointerNearTop && !landingHeader.matches(':hover');
      landingHeader.classList.toggle('is-hidden', shouldHide);
    };

    toggleLandingHeader();
    window.addEventListener('scroll', toggleLandingHeader, { passive: true });
    window.addEventListener('pointermove', (event) => {
      isPointerNearTop = event.clientY <= revealZoneHeight;
      toggleLandingHeader();
    }, { passive: true });
    landingHeader.addEventListener('pointerleave', toggleLandingHeader);
  }

  document.querySelectorAll('.js-scroll-top').forEach(trigger => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

});
