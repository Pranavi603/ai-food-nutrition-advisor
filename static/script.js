document.addEventListener("DOMContentLoaded", function(){

const bmiValue = document.querySelector("b");

if(!bmiValue) return;

const bmi = parseFloat(bmiValue.innerText);

const ctx = document.getElementById('bmiChart');

new Chart(ctx, {
type: 'doughnut',

data: {
labels: ["BMI", "Remaining"],
datasets: [{
data: [bmi, 40-bmi],
backgroundColor: [
"#27ae60",
"#ecf0f1"
]
}]
},

options: {
plugins:{
legend:{display:false}
}
}

});

});