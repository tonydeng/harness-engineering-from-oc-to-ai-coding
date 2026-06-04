// src: https://github.com/JorelAli/mdBook-pagetoc

function forEach(elems, fun) {
    Array.prototype.forEach.call(elems, fun);
}

function getPagetoc() {
    return document.getElementsByClassName("pagetoc")[0];
}

function getPagetocElems() {
    var pagetoc = getPagetoc();
    return pagetoc ? pagetoc.children : [];
}

function getHeaders() {
    return document.getElementsByClassName("header")[0];
}

// Un-active everything when you click it
function forPagetocElem(fun) {
    forEach(getPagetocElems(), fun);
}

function getInt(id) {
    return parseInt(id.substr(1));
}

function onScroll() {
    var pagetoc = getPagetoc();
    if (!pagetoc) {
        return;
    }

    var headers = document.getElementsByClassName("header");
    if (headers.length === 0) {
        return;
    }

    var lastHeader = null;
    for (var i = 0; i < headers.length; i++) {
        var header = headers[i];
        var rect = header.getBoundingClientRect();
        if (rect.top > window.innerHeight) {
            break;
        }
        lastHeader = header;
    }

    if (lastHeader) {
        forPagetocElem(function (el) {
            el.classList.remove("active");
        });
        var active = document.querySelector('.pagetoc a[href="#' + lastHeader.id + '"]');
        if (active) {
            active.classList.add("active");
        }
    }
}

function updatePagetoc() {
    var headers = document.getElementsByClassName("header");
    if (headers.length === 0) {
        return;
    }

    var pagetoc = getPagetoc();
    if (!pagetoc) {
        return;
    }

    pagetoc.innerHTML = "";

    forEach(headers, function (header) {
        var link = document.createElement("a");
        link.href = "#" + header.id;
        link.textContent = header.textContent;
        link.className = header.tagName;
        pagetoc.appendChild(link);
    });

    onScroll();
}

window.addEventListener("scroll", onScroll);

// Update pagetoc when the page changes
var observer = new MutationObserver(updatePagetoc);
var content = document.getElementById("content");
if (content) {
    observer.observe(content, { childList: true });
}

// Initialize pagetoc
updatePagetoc();
