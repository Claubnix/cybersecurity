/**
 * @author      Christian Locher <locher@faithpro.ch>
 * @copyright   2025 Faithful Programming
 * @license     http://www.gnu.org/licenses/gpl-3.0.en.html GNU/GPLv3
 * @version     2025-02-21
**/

function filterNews() {
	articles = document.getElementById("article-holder").getElementsByTagName("article");
	for (let article of articles) {
		query = document.getElementById("searchbar").value.toLowerCase();
		if (article.getElementsByTagName("h3")[0].textContent.toLowerCase().includes(query) || article.getElementsByTagName("p")[0].textContent.toLowerCase().includes(query)) {
			article.style.display = "block";
		} else {
			article.style.display = "none";
		}
	}
}
