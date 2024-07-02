document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const reviewList = document.getElementById('review-list');
    let reviews = [];

    reviewForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;

        const review = { name, rating, comment };
        reviews.push(review);

        displayReviews();
        reviewForm.reset();
    });

    function displayReviews() {
        reviewList.innerHTML = '';
        reviews.forEach(review => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${review.name}</strong> rated us <strong>${review.rating} stars</strong><br>${review.comment}`;
            reviewList.appendChild(li);
        });
    }
});
