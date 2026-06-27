document.addEventListener("DOMContentLoaded", () => {
  // Intersection Observer for scroll reveals
  const revealCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        
        // Find stagger children
        const staggers = entry.target.querySelectorAll(".stagger-item");
        staggers.forEach((item, index) => {
          setTimeout(() => {
            item.classList.add("revealed");
          }, index * 80); // Stagger duration token
          
          // Hover reveal effects inside cards if any
          const arrow = item.querySelector(".arrow-circle");
          if (arrow) {
            arrow.style.transition = "background-color 0.3s ease, color 0.3s ease";
          }
        });
        
        // Unobserve once revealed
        observer.unobserve(entry.target);
      }
    });
  };

  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const observer = new IntersectionObserver(revealCallback, observerOptions);

  const targets = document.querySelectorAll(".reveal-on-scroll");
  targets.forEach(target => observer.observe(target));

  // Count up animation for stats
  const countUp = (element) => {
    const targetVal = parseInt(element.getAttribute("data-target"), 10);
    if (isNaN(targetVal)) return;
    const suffix = element.getAttribute("data-suffix") || "";
    let currentVal = 0;
    const duration = 1000; // ms
    const stepTime = 20; // ms per step
    const steps = duration / stepTime;
    const increment = targetVal / steps;
    
    const timer = setInterval(() => {
      currentVal += increment;
      if (currentVal >= targetVal) {
        element.innerText = targetVal + suffix;
        clearInterval(timer);
      } else {
        element.innerText = Math.floor(currentVal) + suffix;
      }
    }, stepTime);
  };

  // Observe metrics/stats for count-up
  const statsObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counters = entry.target.querySelectorAll(".count-number");
        counters.forEach(counter => countUp(counter));
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  const statsSections = document.querySelectorAll(".stats-trigger");
  statsSections.forEach(section => statsObserver.observe(section));
});
