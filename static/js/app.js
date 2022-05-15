const app = document.querySelector('#app')
var currentlyRendered = []

async function fetchNewPicturesAndRerender() {
    /**
     * Fetching new pictures from the backend
     */
    const res = await fetch("/pics");

    const json = await res.json();

    var picsToRender = json.filter((element) => {

        const isIncluded = currentlyRendered.some((other) => {
            return other.url === element.url;
        })

        return !isIncluded;
    })
    currentlyRendered = json;

    /**
     * Loop through array and render every picture
     */
    picsToRender.forEach(pic => {
        var domPic = document.createElement("img");
        var borderBox = document.createElement("div");
        var subtitle = document.createElement("p");
        domPic.src = pic.url;
        var angle = Math.round(Math.random() * 2)
        domPic.classList = "picture";
        borderBox.classList = `borderbox angle-${angle} animate_animated animate__slideInUp`;
        subtitle.classList = "subtitle animate_animated animate__slideInUp";
        subtitle.innerText = "📸 " + pic.sender + "\n" + pic.subtitle;
        borderBox.appendChild(domPic);
        borderBox.appendChild(subtitle);
        app.appendChild(borderBox);
    })

    /**
     * Overriding currentlyRendered array to track current render status
     */
    currentlyRendered = json;


    /**
     * Scroll to the bottom after pictures have been rendered
     */
    setTimeout(() => {
        window.scroll({
            top: document.body.scrollHeight + 100,
            left: 0,
            behavior: 'smooth'
        })
    }, 1000)

}

fetchNewPicturesAndRerender()

setInterval(() => {
    fetchNewPicturesAndRerender()
}, 5000)