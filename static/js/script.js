const charts = document.querySelectorAll(".chart");

charts.forEach(function (chart) {
  var ctx = chart.getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
        {
          label: "# of Votes",
          data: [12, 19, 3, 5, 2, 3],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});

$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});

/* Animation up on scroll */
const appear1 = new IntersectionObserver((cards) => {
  cards.forEach((card) => {
       console.log(card)
       if(card.isIntersecting) {
            card.target.classList.add("upAlready");
       } else {
            card.target.classList.remove("upAlready");
       }
  });
});
const hiddenElement1 = document.querySelectorAll(".up");
hiddenElement1.forEach((el) => appear1.observe(el));

/* Animation go right on scroll */
const appear2 = new IntersectionObserver((cards) => {
  cards.forEach((card) => {
       console.log(card)
       if(card.isIntersecting) {
            card.target.classList.add("moveRightAlready");
       } else {
            card.target.classList.remove("moveRightAlready");
       }
  });
});
const hiddenElement2 = document.querySelectorAll(".moveRight");
hiddenElement2.forEach((el) => appear2.observe(el));


/* Animation go left on scroll */
const appear3 = new IntersectionObserver((cards) => {
  cards.forEach((card) => {
       console.log(card)
       if(card.isIntersecting) {
            card.target.classList.add("moveLeftAlready");
       } else {
            card.target.classList.remove("moveLeftAlready");
       }
  });
});
const hiddenElement3 = document.querySelectorAll(".moveLeft");
hiddenElement3.forEach((el) => appear3.observe(el));