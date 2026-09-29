function toggleCard(targetCard) {
  console.log("ASDHSADHSADHJKSADJKSAHD");
  const readMoreBtn = targetCard.querySelector('.read-more-btn');
  
  allCards = document.querySelectorAll('.service-card');

  // Close all other cards first
  allCards.forEach(otherCard => {
    if (otherCard !== targetCard) {
      otherCard.setAttribute('data-accordion', 'false');
      otherCard.querySelector('.service-card-content').setAttribute('aria-hidden', 'true');
      otherCard.querySelector('.read-more-btn').textContent = 'Read More';
    }
  });

  // Toggle the clicked card
  if (targetCard.getAttribute('data-accordion') === 'true') {
    targetCard.setAttribute('data-accordion', 'false');
    targetCard.querySelector('.service-card-content').setAttribute('aria-hidden', 'true');
    readMoreBtn.textContent = 'Read More';
  } else {
    targetCard.setAttribute('data-accordion', 'true');
    targetCard.querySelector('.service-card-content').setAttribute('aria-hidden', 'false');
    readMoreBtn.textContent = 'Show Less';
  }
}

function handleHashChange() {
  const hash = window.location.hash;
  console.log(hash);
  
  if (!hash) return;
  
  const target = document.querySelector(hash);
  console.log(target);
  
  if (target?.classList.contains('service-card')) {
    toggleCard(target);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const serviceCards = document.querySelectorAll('.service-card');

  serviceCards.forEach(card => {
    const readMoreBtn = card.querySelector('.read-more-btn');
    
    if (readMoreBtn) {
      readMoreBtn.addEventListener('click', () => toggleCard(card));
    }
  });
});

document.addEventListener('DOMContentLoaded', handleHashChange);
window.addEventListener('hashchange', handleHashChange);
