$(document).ready(function () {
    let currentIndex = 1; // 첫 번째 복제 때문에 1부터 시작
    const sliderInner = $(".slider_inner");
    const slider = $(".slider");
    const sliderCount = slider.length;
    const slideWidth = $(".slider_wrapper").width(); // 부모 크기에 맞춤

    // 마지막 슬라이드 앞에 첫 번째 슬라이드 복제, 첫 번째 앞에 마지막 복제
    sliderInner.prepend(slider.last().clone());
    sliderInner.append(slider.first().clone());

    // 초기 위치 조정
    sliderInner.css("transform", `translateX(${-currentIndex * slideWidth}px)`);

    function moveSlide(index) {
        sliderInner.css("transition", "transform 1.2s ease-in-out");
        sliderInner.css("transform", `translateX(${-index * slideWidth}px)`);
        currentIndex = index;

        // 애니메이션이 끝난 후 무한 루프 처리
        setTimeout(() => {
            if (currentIndex >= sliderCount) {
                sliderInner.css("transition", "none");
                currentIndex = 0;
                sliderInner.css("transform", `translateX(${-currentIndex * slideWidth}px)`);
            } else if (currentIndex <= 0) {
                sliderInner.css("transition", "none");
                currentIndex = sliderCount - 2;
                sliderInner.css("transform", `translateX(${-currentIndex * slideWidth}px)`);
            }
        }, 1200);
    }

    function autoSlide() {
        moveSlide(currentIndex + 1);
    }

    let slideInterval = setInterval(autoSlide, 5000);

    // 반응형 대응: 창 크기 변경 시 슬라이드 너비 재설정
    $(window).resize(function () {
        moveSlide(currentIndex);
    });
});