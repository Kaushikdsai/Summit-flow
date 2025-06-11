const ctx=document.getElementById('hoursChart').getContext('2d');
const rangeType=document.getElementById('range-type');
let chart;
function fetchAndRender(range='days'){
    fetch(`/user-chart?range=${range}`)
    .then(response => response.json())
    .then(data=>{
        rangeType.textContent=range.charAt(0).toUpperCase()+range.slice(1).toLowerCase()
        const labels=data.data.map(item => item.label); //like months
        const values=data.data.map(item => item.value); //hours
        if(chart){
            chart.destroy();
        }
        let backgroundColor;
        if(range=='days'){
            backgroundColor='rgb(0, 0, 225)';
        }
        else if(range=='months'){
            backgroundColor='rgb(225, 183, 0)';
        }
        else{
            backgroundColor='rgb(225,0,0)'
        }
        chart=new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'hours',
                    data: values,
                    backgroundColor: backgroundColor,
                    borderWidth: 1
                }]
            },
            options:{
                scales:{
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: 'rgb(28,186,186)',
                            callback: function(value,index,ticks){
                                const label=this.getLabelForValue(value);
                                if(range=='days'){
                                    return label.split('-')[2];
                                }
                                else{
                                    return label;
                                }
                            }
                        }
                    },
                    y:{
                        beginAtZero: true,
                        min:0,
                        max:0.09,
                        ticks:{
                            color: 'rgb(28,186,186)',
                            stepSize: 0.01
                        }
                    }
                },
                responsive: true,
                plugins:{
                    legend:{
                        display: false
                    }
                }
            }
        });
    })
}
document.addEventListener('DOMContentLoaded', ()=>{
    fetchAndRender();
    document.getElementById('range-select').addEventListener('change',(e)=>{
        fetchAndRender(e.target.value);
    });
});