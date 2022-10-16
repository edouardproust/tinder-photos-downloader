// Show loading bar on btn click (lottie animation)

formBtn = document.querySelector('#formBtn')
loadingDiv = document.querySelector('#loadingBar')

formBtn.addEventListener('click', (e) => {
    loadingDiv.innerHTML = '<lottie-player src="static/img/loading.json" background="transparent" style="width: 500px;" loop autoplay></lottie-player>'
})