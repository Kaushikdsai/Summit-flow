const textarea=document.getElementById('goal-input');
window.addEventListener('DOMContentLoaded',() => {
    const savedVal=localStorage.getItem(`my-goal-${user_id}`);
    if(savedVal){
        textarea.value=savedVal;
    }
});
textarea.addEventListener('input', () => {
    localStorage.setItem(`my-goal-${user_id}`,textarea.value);
});