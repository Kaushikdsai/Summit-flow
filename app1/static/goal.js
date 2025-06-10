const textarea=document.getElementById('goal-input');
window.addEventListener('DOMContentLoaded',() => {
    const savedVal=localStorage.getItem('my-goal');
    if(savedVal){
        textarea.value=savedVal;
    }
});
textarea.addEventListener('input', () => {
    localStorage.setItem('my-goal',textarea.value);
});