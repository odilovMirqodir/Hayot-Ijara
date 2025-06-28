const PAGE_SIZE = 10;
let currentPage = 1;

const tableBody = document.querySelector('#data-table tbody');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const pageInfo = document.getElementById('page-info');

const searchInput = document.getElementById('search-input');
const startDate = document.getElementById('start-date');
const endDate = document.getElementById('end-date');
const filterBtn = document.getElementById('filter-btn');

// Fake dataset
const fakeData = Array.from({ length: 50 }, (_, i) => ({
  id: i+1,
  worker: { username: `user${i+1}`, first_name: `First${i+1}`, last_name: `Last${i+1}` },
  check_in_time: new Date(Date.now() - i*600000).toISOString(),
  location_name: i%2===0 ? 'Main Office' : 'Branch A'
}));

function renderPage(page=1, filters={}) {
  let data = [...fakeData];
  if (filters.search) {
    const s = filters.search.toLowerCase();
    data = data.filter(item =>
      item.worker.username.includes(s) ||
      item.worker.first_name.toLowerCase().includes(s)
    );
  }
  if (filters.start_date) data = data.filter(item => item.check_in_time >= filters.start_date);
  if (filters.end_date) data = data.filter(item => item.check_in_time <= filters.end_date+'T23:59:59');

  const total = data.length;
  const start = (page-1)*PAGE_SIZE;
  const pageItems = data.slice(start, start+PAGE_SIZE);

  tableBody.innerHTML = pageItems.map(item => `
    <tr onclick="goToDetail(${item.id})">
      <td>@${item.worker.username}</td>
      <td>${item.worker.first_name}</td>
      <td>${item.worker.last_name}</td>
      <td>${new Date(item.check_in_time).toLocaleString()}</td>
      <td>${item.location_name}</td>
    </tr>`).join('');

  const totalPages = Math.ceil(total/PAGE_SIZE) || 1;
  pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
  prevBtn.disabled = currentPage<=1;
  nextBtn.disabled = currentPage>=totalPages;
}

prevBtn.addEventListener('click', () => { currentPage--; renderPage(currentPage, getFilters()); });
nextBtn.addEventListener('click', () => { currentPage++; renderPage(currentPage, getFilters()); });
filterBtn.addEventListener('click', () => { currentPage=1; renderPage(currentPage, getFilters()); });

document.addEventListener('DOMContentLoaded', () => renderPage(1, {}));

function getFilters() {
  return {
    search: searchInput.value,
    start_date: startDate.value,
    end_date: endDate.value
  };
}

function goToDetail(id) {
  if (window.location.pathname.includes('worker_detail.html')) return;
  window.location.href = `worker_detail.html?checkin=${id}`;
}

// Detail view
if (document.getElementById('detail-container')) {
  const params = new URLSearchParams(location.search);
  const id = params.get('checkin') || 1;
  const item = fakeData.find(d=>d.id==id) || fakeData[0];
  const div = document.getElementById('detail-container');
  div.innerHTML = `
    <h2>@${item.worker.username}</h2>
    <p><strong>Name:</strong> ${item.worker.first_name} ${item.worker.last_name}</p>
    <p><strong>Time:</strong> ${new Date(item.check_in_time).toLocaleString()}</p>
    <p><strong>Location:</strong> ${item.location_name}</p>
  `;
  document.getElementById('back-btn').onclick = () => history.back();
}
