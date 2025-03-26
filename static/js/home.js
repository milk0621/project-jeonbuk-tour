$(document).ready(function() {
    let currentIndex = 0; 
    const totalSlides = $(".slider").length; 

    function moveSlide() {
        currentIndex++;
        if (currentIndex >= totalSlides) {
            currentIndex = 0; // 마지막 슬라이드 이후 첫 번째로 돌아감
        }
        $(".slider_inner").css("transform", `translateX(${-currentIndex * 100}%)`);
    }
    setInterval(moveSlide, 5000); // 3초마다 슬라이드 전환
});