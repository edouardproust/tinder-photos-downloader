// Show loading bar on btn click (lottie animation)

const formBtn = document.querySelector('#formBtn')
const loadingSpinnerDiv = document.querySelector('#loadingSpinner')
// loadingBarDiv = document.querySelector('#loadingBar')

formBtn.addEventListener('click', (e) => {
    let inner = loadingSpinnerDiv.innerHTML
    if(!inner) {
        loadingSpinnerDiv.innerHTML = '<lottie-player src="static/img/loading-spinner.json" background="transparent" style="height: 50px" loop autoplay></lottie-player>'
        loadingSpinnerDiv.innerHTML += '<div class="small loading-text text-center mt-2">Loading, please wait...</div>'
    }
    // loadingBarDiv.innerHTML = '<lottie-player src="static/img/loading-bar.json" background="transparent" style="height: 150px" loop autoplay></lottie-player>'
})