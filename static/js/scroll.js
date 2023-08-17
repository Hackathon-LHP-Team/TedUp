/* ========== Animations - Floating effect ========== */

/* Animation GO UP on scroll */
const appear1 = new IntersectionObserver((cards) => {
     cards.forEach((card) => {
          console.log(card)
          if (card.isIntersecting) {
               card.target.classList.add("upAlready");
          } else {
               card.target.classList.remove("upAlready");
          }
     });
});
const hiddenElement1 = document.querySelectorAll(".up");
hiddenElement1.forEach((el) => appear1.observe(el));

/* Animation GO RIGHT on scroll */
const appear2 = new IntersectionObserver((cards) => {
     cards.forEach((card) => {
          console.log(card)
          if (card.isIntersecting) {
               card.target.classList.add("moveRightAlready");
          } else {
               card.target.classList.remove("moveRightAlready");
          }
     });
});
const hiddenElement2 = document.querySelectorAll(".moveRight");
hiddenElement2.forEach((el) => appear2.observe(el));


/* Animation GO LEFT on scroll */
const appear3 = new IntersectionObserver((cards) => {
     cards.forEach((card) => {
          console.log(card)
          if (card.isIntersecting) {
               card.target.classList.add("moveLeftAlready");
          } else {
               card.target.classList.remove("moveLeftAlready");
          }
     });
});
const hiddenElement3 = document.querySelectorAll(".moveLeft");
hiddenElement3.forEach((el) => appear3.observe(el));