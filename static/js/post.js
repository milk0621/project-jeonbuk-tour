$(document).ready(function() {
    const text = $('.text');
    const moreText = $('.more-text');
    const lessText = $('.less-text');

    // 더보기 클릭 이벤트
    moreText.on('click', function() {
        moreText.hide(); // 더보기 버튼 숨김
        lessText.show(); // 줄이기 버튼 표시
        text.css('display', 'inline-block'); // 텍스트 표시 변경
    });

    // 줄이기 클릭 이벤트
    lessText.on('click', function() {
        lessText.hide(); // 줄이기 버튼 숨김
        moreText.show(); // 더보기 버튼 표시
        text.css('display', '-webkit-box'); // 텍스트 속성 원래대로 변경
    });
});

