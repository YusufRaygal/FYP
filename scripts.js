/--index.html-/

window.onscroll = function () {
    var footer = document.querySelector('.footer');
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        footer.classList.add('visible');
    } else {
        footer.classList.remove('visible');
    }
};

document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('mouseover', function () {
        const content = this.getAttribute('data-content');
        if (content) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = content;
            document.body.appendChild(tooltip);
            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.bottom}px`;
            tooltip.style.left = `${rect.left}px`;
        }
    });

    link.addEventListener('mouseout', function () {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    });
});
/--index.html-/

// /login.js-/
const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener('click', () =>{
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () =>{
    container.classList.remove("sign-up-mode");
});
/--Login.js-/