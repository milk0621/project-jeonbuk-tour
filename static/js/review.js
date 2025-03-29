//적용안됨, flask로 화면 구현 후 제작
$(document).ready(function() {
    const reviewText = $('.review-text');
    const moreReview = $('.more-review');
    const reviewAdd = $('.review-add');

    moreReview.on('click', function() {
        reviewAdd.removeClass();
        reviewAdd.addClass('add');
    });
});