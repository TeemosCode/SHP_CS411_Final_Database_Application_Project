console.log("Hello World!");


// before scrolling, check to see if user started off on the top. If so color the navbar for the home button.
// let startingPosition = document.body.scrollTop || document.documentElement.scrollTop;
// if (startingPosition == 0) {
// 	document.getElementById("section0").classList.add("navbar_active");
// }

window.onscroll = function() {
	scrollFunction();
}

// section0 is the original navhome (It was also updated in scss file)


var sectionlist = document.getElementsByTagName("section"); // list of all sections
var preActiveNavbar = document.getElementById("section0");
// var scrollBarHeight = document.getElementById("navlists").offsetHeight;
// //  53 <-> 212px
// console.log(scrollBarHeight);

var showcase = document.getElementById("showcase");
var slideshow = document.getElementById("slideshow");
var about = document.getElementById("about");
var sign_up = document.getElementById("sign-up");



function removeActiveNavbar(list, className) {
	if (list.length != 0) {
		list[0].classList.remove(className);
	}
}


function scrollFunction() {
		var showcaseHeight = showcase.offsetHeight; // Paddies navbar
		var slideshowHeight = slideshow.offsetHeight; // features navbar
		var aboutHeight = about.offsetHeight; // about (three slices) navbar
		var sign_upHeight = sign_up.offsetHeight; // last signup background navbar

		
		var curPosition = document.documentElement.scrollTop || document.body.scrollTop;

		if (curPosition > 100 || document.body.scrollTop > 100) {
			document.getElementById("navlists").style.margin="-7px auto";
			document.getElementById("section0").style.fontSize = "14px";
		} else {
			document.getElementById("navlists").style.margin="0 auto";
			document.getElementById("section0").style.fontSize="23px";
		}

		// Navigation between different sections
		// Upon entering a new section (calculate for every sections)
		var navBarHeight = document.getElementsByClassName('container')[0].offsetHeight;
		var navBarBottom = curPosition + navBarHeight;
		var prevActiveNavList = document.getElementsByClassName("navbar_active");

		if (navBarBottom >= 0 && navBarBottom < showcaseHeight) {
			removeActiveNavbar(prevActiveNavList, "navbar_active");
			document.getElementById("section0").classList.add("navbar_active");
		} else if ((window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 50)) { /////// BIG PROBELM HERE TO DIG INTO ABOUT THE LOGIC!!!!
			removeActiveNavbar(prevActiveNavList, "navbar_active"); // If we put this just before the last else statement or make it a seperate if above all this, the shiit won't work like wtf??!
			document.getElementById("section1").classList.add("navbar_active");
		} else if (navBarBottom >= showcaseHeight && navBarBottom < (showcaseHeight + slideshowHeight)) {
			removeActiveNavbar(prevActiveNavList, "navbar_active");
			document.getElementById("section3").classList.add("navbar_active");
		} else if (navBarBottom >= (showcaseHeight + slideshowHeight) && navBarBottom < (showcaseHeight + slideshowHeight + aboutHeight)) {
			removeActiveNavbar(prevActiveNavList, "navbar_active");
			document.getElementById("section2").classList.add("navbar_active");
		} else {
			removeActiveNavbar(prevActiveNavList, "navbar_active");
			document.getElementById("section1").classList.add("navbar_active");
		}
		// console.log("++++" + (window.innerHeight + window.scrollY) + "-------" + (document.body.scrollHeight- 30));
		// console.log((window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 20));
}

// //
// if (document.getElementById("detail").offsetTop-document.getElementById("navBar").offsetHeight > document.documentElement.scrollTop) {
//         document.getElementById("#intro").style.backgroundColor="black"
//         document.getElementById("#detail").style.backgroundColor="transparent"
//         document.getElementById("#contact").style.backgroundColor="transparent"
// } else if (document.getElementById("detail").offsetTop-document.getElementById("navBar").offsetHeight < document.documentElement.scrollTop && document.documentElement.scrollTop < document.getElementById("contact").offsetTop-window.innerHeight) {
//         document.getElementById("#intro").style.backgroundColor="transparent"
//         document.getElementById("#detail").style.backgroundColor="black"
//         document.getElementById("#contact").style.backgroundColor="transparent"
//   } else {
//         document.getElementById("#intro").style.backgroundColor="transparent"
//         document.getElementById("#detail").style.backgroundColor="transparent"
//         document.getElementById("#contact").style.backgroundColor="black"
//   }


function changecolor() {
	document.body.style.backgroundColor = 'red';
}


let button = document.getElementById("changecolor");
if (button == null) {
	console.log("No more change me button! SAD!");
} else {
	button.addEventListener('click', function () {
		var clicked = document.getElementById("changecolor");
		if (clicked.style.className == "1") {
			document.body.style.backgroundColor='white';
			clicked.style.className = "0"
		} else {
			document.body.style.backgroundColor='red';
			clicked.style.className = "1";
		}
	});
}


/* Slide functions for carousel buttons */

var slideIndex = 0;
showSlides(slideIndex); // Display the first slide first on load

function switchSlides(index) {
	showSlides(slideIndex += index);
}

function showSlides(index) {
	var slides = document.getElementsByClassName("slides");
	if (index >= slides.length) {
		slideIndex = 0;
	}
	if (index < 0) {
		slideIndex = slides.length - 1;
	}
	for (var i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	slides[slideIndex].style.display = "block";
}



// add the function to the click events of the arrow buttons for carousel
let leftArrowButton = document.getElementById("leftArrow");
// leftArrowButton.addEventListener("click", switchSlides(-1));
leftArrowButton.addEventListener('click', function () {
	slideIndex -= 1;
	var slides = document.getElementsByClassName("slides");
	if (slideIndex >= slides.length) {
		slideIndex = 0;
	}
	if (slideIndex < 0) {
		slideIndex = slides.length - 1;
	}
	for (var i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	slides[slideIndex].style.display = "block";
});

let rightArrowButton = document.getElementById("rightArrow");
// rightArrowButton.addEventListener("click", switchSlides(1));
rightArrowButton.addEventListener('click', function () {
	slideIndex += 1;
	var slides = document.getElementsByClassName("slides");
	if (slideIndex >= slides.length) {
		slideIndex = 0;
	}
	if (slideIndex < 0) {
		slideIndex = slides.length - 1;
	}
	for (var i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	slides[slideIndex].style.display = "block";
});


// Modal handling
// Get the modal
let modalList = document.getElementsByClassName("modal");
console.log(modalList);
let modalOpenButtonList = document.getElementsByClassName("openModal");

// Using loops to add click events
for (let i = 0; i < modalOpenButtonList.length; i++) {
	modalOpenButtonList[i].addEventListener('click', function() {
		modalList[0].style.display = "block";
	});
}

// Using loops to add click events
var modalCloseButtonList = document.getElementsByClassName("modal-close");
for (let i = 0; i < modalCloseButtonList.length; i++) {
	console.log(modalCloseButtonList[i]);
	console.log(modalList[i]);
	modalCloseButtonList[i].addEventListener('click', function() {
		modalList[i].style.display = "none";
	});
}


window.onclick = function(event) {
	if (event.target == modalList[0]) {
		modalList[0].style.display = "none";
	} else if (event.target == modalList[1]) {
		modalList[1].style.display = "none";
	} else if (event.target == modalList[2]) {
		modalList[2].style.display = "none";
	}
}
