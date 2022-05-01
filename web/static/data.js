export const data = {
    labels: ['1', '2', '3', '4', '5', '6'],
    datasets: [
      {
        label: 'Nombre de buts',
        data: [1, 2, 4, 6, 7, 10],
        fill: false,
        backgroundColor: 'white',
        borderColor: "#0190F8",
      },
    ],
  };

export const dataPass = {
    labels: ['1', '2', '3', '4', '5', '6'],
    datasets: [
      {
        label: 'Nombre de passes',
        data: [40, 70, 104, 121, 154, 180],
        fill: false,
        backgroundColor: 'white',
        borderColor: "#0190F8",
      },
    ],
};

export const dataVictory = {
    labels: ['Défaite', 'Victoire'],
    datasets: [
      {
        label: 'Ratio Défaite/Victoire',
        data: [2, 4],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(75, 192, 192, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

export const options = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  };