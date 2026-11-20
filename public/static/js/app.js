/**
 * Big 4 Accounting Firms News Hub - Client Application
 * 삼일 PwC, 삼정 KPMG, 한영 EY, 안진 Deloitte 뉴스 수집 및 인터랙션 모듈
 */

const STATE = {
  currentFirm: 'all',
  searchQuery: '',
  selectedSource: '',
  selectedCategory: '',
  currentSort: 'latest',
  currentPage: 1,
  limit: 12,
  totalPages: 1,
  totalItems: 0,
  bookmarks: JSON.parse(localStorage.getItem('big4_bookmarks') || '[]'),
  isBookmarkMode: false,
  firmsMeta: {},
  cachedNewsList: [],
  charts: {}
};

// 회계법인별 배너 및 브랜딩 테마 설정
const FIRM_THEMES = {
  all: {
    title: '전체 빅4 뉴스 종합',
    badge: 'Big 4 Korea',
    desc: '삼일 PwC, 삼정 KPMG, 한영 EY, 안진 Deloitte 등 국내 4대 회계법인의 최신 기사를 한눈에 모아봅니다.',
    gradient: 'from-slate-900 to-indigo-950',
    color: '#0f172a'
  },
  samil: {
    title: '삼일 PwC (Samil PwC)',
    badge: '국내 1위 회계법인',
    desc: '신뢰 구축과 지속가능한 성장을 추구하는 삼일PwC의 회계감사, 딜(M&A) 자문, 세무, AI 혁신 뉴스입니다.',
    gradient: 'from-[#8a2200] via-[#c23e00] to-[#e05307]',
    leader: '윤훈수 대표',
    founded: '1971년',
    color: '#e05307'
  },
  samjong: {
    title: '삼정 KPMG (Samjong KPMG)',
    badge: '지식과 신뢰의 파트너',
    desc: '비즈니스 통찰력과 고도화된 컨설팅 역량을 선보이는 삼정KPMG의 주요 리포트, 금융 및 산업 자문 뉴스입니다.',
    gradient: 'from-[#00225c] via-[#003882] to-[#0051C7]',
    leader: '김교태 대표',
    founded: '1969년',
    color: '#0051C7'
  },
  ey: {
    title: '한영 EY (EY Han Young)',
    badge: '더 나은 세상 만들기',
    desc: 'EY-파르테논의 전략 자문, EY.ai 솔루션 및 글로벌 지속가능성(ESG) 선도 소식을 전달합니다.',
    gradient: 'from-[#422006] via-[#78350f] to-[#b45309]',
    leader: '박용근 대표',
    founded: '1989년',
    color: '#b45309'
  },
  deloitte: {
    title: '안진 Deloitte (Deloitte Anjin)',
    badge: '최고의 전문가 그룹',
    desc: '강력한 글로벌 네트워크와 테크놀로지 자문, 리스크 관리를 이끄는 딜로이트 안진의 최신 보도입니다.',
    gradient: 'from-[#052e16] via-[#14532d] to-[#007624]',
    leader: '홍종성 대표',
    founded: '1987년',
    color: '#007624'
  }
};

// 회계법인별 카드 뱃지 스타일 매핑
const FIRM_BADGE_STYLES = {
  samil: {
    bg: 'bg-orange-100 dark:bg-orange-950/70 text-orange-700 dark:text-orange-300 border border-orange-200 dark:border-orange-800',
    dot: 'bg-[#e05307]',
    name: '삼일 PwC'
  },
  samjong: {
    bg: 'bg-blue-100 dark:bg-blue-950/70 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800',
    dot: 'bg-[#0051C7]',
    name: '삼정 KPMG'
  },
  ey: {
    bg: 'bg-amber-100 dark:bg-amber-950/70 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800',
    dot: 'bg-[#b45309]',
    name: '한영 EY'
  },
  deloitte: {
    bg: 'bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800',
    dot: 'bg-[#007624]',
    name: '안진 Deloitte'
  },
  all: {
    bg: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700',
    dot: 'bg-slate-500',
    name: '전체 빅4'
  }
};

// HTML 이스케이프: 외부 RSS에서 온 제목/요약/언론사명에 따옴표나 <, > 가 있어도
// 화면이 깨지거나 스크립트가 실행되지 않도록 모든 동적 텍스트는 이 함수를 거친다.
function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));
}

// 원문 링크는 http(s)만 허용 (javascript: 등 차단)
function safeUrl(url) {
  return /^https?:\/\//i.test(url || '') ? url : '#';
}

// API 주소 생성.
// Vercel 에서 /api/news 같은 하위 경로가 함수로 전달되지 않아 HTML 이 돌아오던 문제를 피하기 위해
// 항상 함수 파일 경로(/api/index)로 호출하고 실제 엔드포인트는 __route 쿼리로 전달한다.
function apiUrl(route, query = '') {
  return `/api/index?__route=${route}` + (query ? `&${query}` : '');
}

// 응답이 뒤바뀌어 도착해도 가장 마지막 요청의 결과만 화면에 반영하기 위한 카운터
let newsRequestSeq = 0;

// 초기화
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  updateBookmarkCountBadge();
  fetchFirms();
  fetchNews();
  lucide.createIcons();
});

// 테마 관리 (다크/라이트)
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  lucide.createIcons();
}

// 회계법인 메타데이터 로드
async function fetchFirms() {
  try {
    const res = await fetch(apiUrl('firms'));
    const data = await res.json();
    if (data.success && data.firms) {
      data.firms.forEach(firm => {
        STATE.firmsMeta[firm.id] = firm;
        const countEl = document.getElementById(`count-${firm.id}`);
        if (countEl) countEl.innerText = firm.news_count;
      });
      updateBanner();
    }
  } catch (err) {
    console.error('Failed to fetch firms info:', err);
  }
}

// 뉴스 목록 로드
async function fetchNews() {
  showLoading(true);

  if (STATE.isBookmarkMode) {
    // 북마크 모드인 경우
    renderBookmarkNews();
    showLoading(false);
    return;
  }

  const params = new URLSearchParams({
    firm: STATE.currentFirm,
    q: STATE.searchQuery,
    source: STATE.selectedSource,
    category: STATE.selectedCategory,
    sort: STATE.currentSort,
    page: STATE.currentPage,
    limit: STATE.limit
  });

  const seq = ++newsRequestSeq;

  try {
    const res = await fetch(apiUrl('news', params.toString()));
    const data = await res.json();

    if (seq !== newsRequestSeq) return; // 더 최신 요청이 있으면 이 응답은 버린다

    if (data.success) {
      STATE.cachedNewsList = data.news;
      STATE.totalItems = data.total;
      STATE.totalPages = data.total_pages;

      renderNewsGrid(data.news);
      renderPagination(data.total, data.page, data.total_pages);
      updateFacets(data.facets);
      updateResultCount(data.total);
    }
  } catch (err) {
    console.error('Failed to fetch news:', err);
    if (seq === newsRequestSeq) showToast('뉴스 데이터를 불러오지 못했습니다.');
  } finally {
    if (seq === newsRequestSeq) showLoading(false);
  }
}

// 뉴스 카드 렌더링
function renderNewsGrid(newsList) {
  const grid = document.getElementById('newsGrid');
  const empty = document.getElementById('emptyState');

  if (!newsList || newsList.length === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }

  empty.classList.add('hidden');
  grid.innerHTML = newsList.map(item => createNewsCardHTML(item)).join('');
  lucide.createIcons();
}

function createNewsCardHTML(item) {
  const firmStyle = FIRM_BADGE_STYLES[item.firm] || FIRM_BADGE_STYLES.all;
  const isBookmarked = STATE.bookmarks.includes(item.id);
  const timeAgo = formatTimeAgo(item.pub_date);

  const tagsHTML = (item.tags || []).slice(0, 3).map(tag => `
    <span data-tag="${esc(tag)}" onclick="searchByTag(this.dataset.tag, event)" class="inline-block px-2 py-0.5 text-[11px] font-medium rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-blue-50 hover:text-blue-600 dark:hover:bg-blue-950/60 dark:hover:text-blue-300 transition cursor-pointer">
      #${esc(tag)}
    </span>
  `).join('');

  return `
    <article class="news-card flex flex-col justify-between bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm relative group" data-id="${esc(item.id)}" onclick="openArticleModal(this.dataset.id)">
      
      <div>
        <!-- 카드 상단 메타 바 -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center space-x-2">
            <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${firmStyle.bg}">
              <span class="w-1.5 h-1.5 rounded-full ${firmStyle.dot}"></span>
              <span>${esc(item.firm_name || firmStyle.name)}</span>
            </span>
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400 truncate max-w-[110px]" title="${esc(item.source)}">
              ${esc(item.source)}
            </span>
          </div>

          <div class="flex items-center space-x-1">
            <span class="text-[11px] text-slate-400 dark:text-slate-500 whitespace-nowrap">
              ${timeAgo}
            </span>
            <!-- 북마크 버튼 -->
            <button data-id="${esc(item.id)}" onclick="toggleBookmark(this.dataset.id, event)" class="p-1 rounded-lg text-slate-400 hover:text-amber-500 transition" title="스크랩">
              <i data-lucide="bookmark" class="w-4 h-4 ${isBookmarked ? 'fill-amber-500 text-amber-500' : ''}"></i>
            </button>
          </div>
        </div>

        <!-- 기사 제목 -->
        <h3 class="text-base font-bold text-slate-900 dark:text-white line-clamp-2 leading-snug group-hover:text-blue-600 dark:group-hover:text-blue-400 transition mb-2">
          ${esc(item.title)}
        </h3>

        <!-- 기사 요약 -->
        <p class="text-xs text-slate-600 dark:text-slate-400 line-clamp-3 leading-relaxed mb-4">
          ${esc(item.summary)}
        </p>
      </div>

      <!-- 카드 하단 태그 및 액션 링크 -->
      <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between mt-auto">
        <div class="flex flex-wrap gap-1">
          ${tagsHTML}
        </div>

        <a href="${esc(safeUrl(item.url))}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" class="p-1.5 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition flex items-center space-x-1 text-xs" title="원문 기사 새 탭으로 보기">
          <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
        </a>
      </div>

    </article>
  `;
}

// 상단 배너 업데이트
function updateBanner() {
  const theme = FIRM_THEMES[STATE.currentFirm] || FIRM_THEMES.all;
  const banner = document.getElementById('firmBanner');
  const title = document.getElementById('bannerTitle');
  const badge = document.getElementById('bannerBadge');
  const desc = document.getElementById('bannerDesc');
  const totalCount = document.getElementById('metaTotalCount');
  const leaderBox = document.getElementById('metaLeaderBox');
  const leader = document.getElementById('metaLeader');
  const yearBox = document.getElementById('metaYearBox');
  const year = document.getElementById('metaYear');

  banner.className = `bg-gradient-to-r ${theme.gradient} text-white transition-all duration-300`;
  title.innerText = theme.title;
  badge.innerText = theme.badge;
  desc.innerText = theme.desc;

  const firmMeta = STATE.firmsMeta[STATE.currentFirm];
  if (firmMeta && STATE.currentFirm !== 'all') {
    leaderBox.classList.remove('hidden');
    leader.innerText = firmMeta.ceo || '-';
    yearBox.classList.remove('hidden');
    year.innerText = firmMeta.founded || '-';
    totalCount.innerText = `${firmMeta.news_count || 0}건`;
  } else {
    leaderBox.classList.add('hidden');
    yearBox.classList.add('hidden');
    totalCount.innerText = `${STATE.firmsMeta.all?.news_count || 0}건`;
  }
}

// 회계법인 탭 전환
function switchFirm(firmId) {
  if (STATE.isBookmarkMode) {
    STATE.isBookmarkMode = false;
    document.getElementById('bookmarkModeNotice').classList.add('hidden');
    clearBookmarkTabHighlight();
  }

  STATE.currentFirm = firmId;
  STATE.currentPage = 1;

  // 탭 활성화 스타일 업데이트
  document.querySelectorAll('.firm-tab-btn').forEach(btn => {
    if (btn.getAttribute('data-firm') === firmId) {
      btn.classList.add('active-tab');
    } else {
      btn.classList.remove('active-tab');
    }
  });

  updateBanner();
  fetchNews();
}

// 카테고리 선택
function selectCategory(cat) {
  STATE.selectedCategory = cat;
  STATE.currentPage = 1;

  document.querySelectorAll('.category-chip').forEach(chip => {
    if (chip.getAttribute('data-category') === cat) {
      chip.classList.add('active');
    } else {
      chip.classList.remove('active');
    }
  });

  fetchNews();
}

// 태그 클릭 시 즉시 검색
function searchByTag(tag, event) {
  if (event) event.stopPropagation();
  const input = document.getElementById('searchInput');
  input.value = tag;
  handleSearchInput({ target: { value: tag } });
}

// 검색어 입력 디바운스
let searchTimeout = null;
function handleSearchInput(e) {
  const query = e.target.value.trim();
  const clearBtn = document.getElementById('clearSearchBtn');
  clearBtn.classList.toggle('hidden', query.length === 0);

  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    STATE.searchQuery = query;
    STATE.currentPage = 1;
    fetchNews();
  }, 300);
}

function clearSearch() {
  const input = document.getElementById('searchInput');
  input.value = '';
  document.getElementById('clearSearchBtn').classList.add('hidden');
  STATE.searchQuery = '';
  STATE.currentPage = 1;
  fetchNews();
}

function handleSourceChange() {
  STATE.selectedSource = document.getElementById('sourceSelect').value;
  STATE.currentPage = 1;
  fetchNews();
}

function handleSortChange() {
  STATE.currentSort = document.getElementById('sortSelect').value;
  STATE.currentPage = 1;
  fetchNews();
}

function resetAllFilters() {
  STATE.currentFirm = 'all';
  STATE.searchQuery = '';
  STATE.selectedSource = '';
  STATE.selectedCategory = '';
  STATE.currentSort = 'latest';
  STATE.currentPage = 1;
  STATE.isBookmarkMode = false;

  document.getElementById('searchInput').value = '';
  document.getElementById('clearSearchBtn').classList.add('hidden');
  document.getElementById('sourceSelect').value = '';
  document.getElementById('sortSelect').value = 'latest';
  document.getElementById('bookmarkModeNotice').classList.add('hidden');
  clearBookmarkTabHighlight();

  document.querySelectorAll('.firm-tab-btn').forEach(b => b.classList.toggle('active-tab', b.getAttribute('data-firm') === 'all'));
  document.querySelectorAll('.category-chip').forEach(c => c.classList.toggle('active', c.getAttribute('data-category') === ''));

  updateBanner();
  fetchNews();
}

// 언론사 셀렉트박스 옵션 동적 업데이트
function updateFacets(facets) {
  if (!facets || !facets.sources) return;
  const select = document.getElementById('sourceSelect');
  const currentValue = STATE.selectedSource;

  const sources = facets.sources.slice();
  // 선택해 둔 언론사가 현재 조건에서 0건이어도 선택 상태가 화면에서 사라지지 않게 유지
  if (currentValue && !sources.some(([name]) => name === currentValue)) {
    sources.push([currentValue, 0]);
  }

  let optionsHTML = '<option value="">모든 언론사 (전체)</option>';
  sources.forEach(([name, count]) => {
    const isSelected = name === currentValue ? 'selected' : '';
    optionsHTML += `<option value="${esc(name)}" ${isSelected}>${esc(name)} (${count})</option>`;
  });
  select.innerHTML = optionsHTML;
}

// 결과 개수 텍스트 표시
function updateResultCount(total) {
  const countText = document.getElementById('resultCountText');
  countText.innerHTML = `총 <strong>${total}</strong>건의 기사`;

  const badge = document.getElementById('activeFilterBadge');
  const activeFilters = [];
  if (STATE.currentFirm !== 'all') activeFilters.push(FIRM_THEMES[STATE.currentFirm]?.title || STATE.currentFirm);
  if (STATE.selectedCategory) activeFilters.push(STATE.selectedCategory);
  if (STATE.selectedSource) activeFilters.push(STATE.selectedSource);
  if (STATE.searchQuery) activeFilters.push(`'${STATE.searchQuery}'`);

  if (activeFilters.length > 0) {
    badge.innerText = `적용 필터: ${activeFilters.join(' > ')}`;
    badge.classList.remove('hidden');
  } else {
    badge.classList.add('hidden');
  }
}

// 페이지네이션 렌더링
function renderPagination(total, page, totalPages) {
  const container = document.getElementById('pagination');
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = '';

  // 이전 버튼
  html += `
    <button onclick="goToPage(${page - 1})" ${page <= 1 ? 'disabled' : ''} class="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-semibold transition flex items-center space-x-1 ${page <= 1 ? 'opacity-40 cursor-not-allowed' : 'hover:bg-slate-100 dark:hover:bg-slate-800'}">
      <i data-lucide="chevron-left" class="w-4 h-4"></i>
      <span class="hidden sm:inline">이전</span>
    </button>
  `;

  // 페이지 번호들
  const maxButtons = 5;
  let startPage = Math.max(1, page - Math.floor(maxButtons / 2));
  let endPage = Math.min(totalPages, startPage + maxButtons - 1);
  if (endPage - startPage + 1 < maxButtons) {
    startPage = Math.max(1, endPage - maxButtons + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    const isActive = i === page;
    html += `
      <button onclick="goToPage(${i})" class="w-9 h-9 rounded-xl text-xs font-bold transition ${
        isActive 
          ? 'bg-blue-600 text-white shadow-sm' 
          : 'border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
      }">
        ${i}
      </button>
    `;
  }

  // 다음 버튼
  html += `
    <button onclick="goToPage(${page + 1})" ${page >= totalPages ? 'disabled' : ''} class="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-semibold transition flex items-center space-x-1 ${page >= totalPages ? 'opacity-40 cursor-not-allowed' : 'hover:bg-slate-100 dark:hover:bg-slate-800'}">
      <span class="hidden sm:inline">다음</span>
      <i data-lucide="chevron-right" class="w-4 h-4"></i>
    </button>
  `;

  container.innerHTML = html;
  lucide.createIcons();
}

function goToPage(page) {
  if (page < 1 || page > STATE.totalPages) return;
  STATE.currentPage = page;
  fetchNews();
  scrollToTop();
}

// 북마크 토글 및 모아보기
function toggleBookmark(articleId, event) {
  if (event) event.stopPropagation();

  const idx = STATE.bookmarks.indexOf(articleId);
  if (idx > -1) {
    STATE.bookmarks.splice(idx, 1);
    showToast('스크랩을 취소했습니다.');
  } else {
    STATE.bookmarks.push(articleId);
    showToast('기사를 내 스크랩에 저장했습니다.');
  }

  localStorage.setItem('big4_bookmarks', JSON.stringify(STATE.bookmarks));
  updateBookmarkCountBadge();

  if (STATE.isBookmarkMode) {
    renderBookmarkNews();
  } else {
    fetchNews();
  }
}

function updateBookmarkCountBadge() {
  const badge = document.getElementById('bookmarkCountBadge');
  if (badge) badge.innerText = STATE.bookmarks.length;
}

function clearBookmarkTabHighlight() {
  const btn = document.getElementById('bookmarkTabBtn');
  if (btn) btn.classList.remove('bg-amber-100', 'dark:bg-amber-950/50', 'text-amber-800');
}

function toggleBookmarkMode() {
  STATE.isBookmarkMode = !STATE.isBookmarkMode;
  const notice = document.getElementById('bookmarkModeNotice');
  const btn = document.getElementById('bookmarkTabBtn');

  if (STATE.isBookmarkMode) {
    notice.classList.remove('hidden');
    btn.classList.add('bg-amber-100', 'dark:bg-amber-950/50', 'text-amber-800');
    renderBookmarkNews();
  } else {
    notice.classList.add('hidden');
    clearBookmarkTabHighlight();
    fetchNews();
  }
}

async function renderBookmarkNews() {
  showLoading(true);
  document.getElementById('pagination').innerHTML = '';

  if (STATE.bookmarks.length === 0) {
    STATE.cachedNewsList = [];
    renderNewsGrid([]);
    updateResultCount(0);
    showLoading(false);
    return;
  }

  try {
    // 전체 목록의 앞 50건만 받아 걸러내던 방식 대신, 스크랩한 기사 id로 직접 조회한다.
    const params = new URLSearchParams({ ids: STATE.bookmarks.join(','), limit: 200 });
    const res = await fetch(apiUrl('news', params.toString()));
    const data = await res.json();
    if (data.success) {
      STATE.cachedNewsList = data.news;   // 기사 상세 모달이 이 목록에서 기사를 찾는다
      renderNewsGrid(data.news);
      updateResultCount(data.news.length);
    }
  } catch (e) {
    console.error(e);
    showToast('스크랩을 불러오지 못했습니다.');
  } finally {
    showLoading(false);
  }
}

// 실시간 수집 새로고침 실행
async function triggerRefresh() {
  const icon = document.getElementById('refreshIcon');
  icon.classList.add('animate-spin-fast');

  showToast('최신 빅4 회계법인 뉴스를 실시간 수집 중입니다...');

  try {
    const res = await fetch(apiUrl('refresh'), { method: 'POST' });
    const data = await res.json();

    if (data.success) {
      const failed = (data.errors || []).length;
      showToast(
        failed > 0
          ? `일부 언론 피드 수집에 실패했습니다 (${failed}건). 총 ${data.total}건 표시 중`
          : `뉴스 수집 완료! 신규 ${data.crawled_count}건 반영, 총 ${data.total}건`
      );
      fetchFirms();
      fetchNews();
    } else {
      // 실시간 수집이 전부 실패한 경우 (네트워크 차단, 구글 뉴스 접속 제한 등)
      showToast('실시간 뉴스를 가져오지 못했습니다. 기존 저장된 기사를 보여드립니다.');
    }
  } catch (err) {
    showToast('새로고침 중 오류가 발생했습니다.');
  } finally {
    icon.classList.remove('animate-spin-fast');
  }
}

// 기사 상세 보기 모달
let currentModalArticle = null;
function openArticleModal(articleId) {
  const article = STATE.cachedNewsList.find(a => a.id === articleId);
  if (!article) return;

  currentModalArticle = article;
  const modal = document.getElementById('articleModal');
  const firmStyle = FIRM_BADGE_STYLES[article.firm] || FIRM_BADGE_STYLES.all;

  const firmBadge = document.getElementById('modalFirmBadge');
  firmBadge.className = `text-xs px-2.5 py-1 rounded-full font-bold ${firmStyle.bg}`;
  firmBadge.innerText = article.firm_name || firmStyle.name;

  document.getElementById('modalSourceBadge').innerText = article.source || '종합뉴스';
  document.getElementById('modalDate').innerText = formatAbsoluteDate(article.pub_date);
  document.getElementById('modalTitle').innerText = article.title;
  document.getElementById('modalSummary').innerText = article.summary;

  // 태그
  const tagsContainer = document.getElementById('modalTags');
  tagsContainer.innerHTML = (article.tags || []).map(tag => `
    <span class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
      #${esc(tag)}
    </span>
  `).join('');

  // 북마크 버튼
  updateModalBookmarkBtn();

  // 원문 링크
  const extLink = document.getElementById('modalExternalLink');
  extLink.href = safeUrl(article.url);

  modal.classList.remove('hidden');
  lucide.createIcons();
}

function updateModalBookmarkBtn() {
  if (!currentModalArticle) return;
  const isBookmarked = STATE.bookmarks.includes(currentModalArticle.id);
  const icon = document.getElementById('modalBookmarkIcon');
  const text = document.getElementById('modalBookmarkText');

  if (isBookmarked) {
    icon.classList.add('fill-amber-500', 'text-amber-500');
    text.innerText = '스크랩 취소';
  } else {
    icon.classList.remove('fill-amber-500', 'text-amber-500');
    text.innerText = '스크랩 저장';
  }
}

function toggleModalBookmark() {
  if (!currentModalArticle) return;
  toggleBookmark(currentModalArticle.id);
  updateModalBookmarkBtn();
}

function closeArticleModal() {
  document.getElementById('articleModal').classList.add('hidden');
  currentModalArticle = null;
}

// 통계 모달 열기 및 차트 렌더링
async function openStatsModal() {
  const modal = document.getElementById('statsModal');
  modal.classList.remove('hidden');

  try {
    const res = await fetch(apiUrl('stats'));
    const stats = await res.json();
    if (stats.success) {
      renderCharts(stats);
      renderTopTags(stats.top_tags);
    }
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

function closeStatsModal() {
  document.getElementById('statsModal').classList.add('hidden');
}

function renderCharts(stats) {
  // 기존 차트 파괴
  if (STATE.charts.firm) STATE.charts.firm.destroy();
  if (STATE.charts.category) STATE.charts.category.destroy();
  if (STATE.charts.source) STATE.charts.source.destroy();

  const isDark = document.documentElement.classList.contains('dark');
  const textColor = isDark ? '#94a3b8' : '#475569';

  // 1. 회계법인 점유율 도넛 차트
  const ctxFirm = document.getElementById('firmChart').getContext('2d');
  STATE.charts.firm = new Chart(ctxFirm, {
    type: 'doughnut',
    data: {
      labels: stats.firms_distribution.labels,
      datasets: [{
        data: stats.firms_distribution.data,
        backgroundColor: stats.firms_distribution.colors,
        borderWidth: 2,
        borderColor: isDark ? '#0f172a' : '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: textColor, font: { size: 11 } } }
      }
    }
  });

  // 2. 카테고리별 분포 바 차트
  const ctxCat = document.getElementById('categoryChart').getContext('2d');
  STATE.charts.category = new Chart(ctxCat, {
    type: 'bar',
    data: {
      labels: stats.categories_distribution.labels,
      datasets: [{
        label: '기사 수',
        data: stats.categories_distribution.data,
        backgroundColor: '#3b82f6',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: textColor, font: { size: 10 } }, grid: { display: false } },
        y: { ticks: { color: textColor, precision: 0 }, grid: { color: isDark ? '#1e293b' : '#f1f5f9' } }
      },
      plugins: { legend: { display: false } }
    }
  });

  // 3. 언론사별 차트
  const ctxSrc = document.getElementById('sourceChart').getContext('2d');
  STATE.charts.source = new Chart(ctxSrc, {
    type: 'bar',
    data: {
      labels: stats.top_sources.labels,
      datasets: [{
        label: '보도 건수',
        data: stats.top_sources.data,
        backgroundColor: '#f59e0b',
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: textColor, precision: 0 }, grid: { color: isDark ? '#1e293b' : '#f1f5f9' } },
        y: { ticks: { color: textColor, font: { size: 10 } }, grid: { display: false } }
      },
      plugins: { legend: { display: false } }
    }
  });
}

function renderTopTags(tags) {
  const container = document.getElementById('topTagsContainer');
  if (!tags || tags.length === 0) {
    container.innerHTML = '<span class="text-xs text-slate-400">태그 정보가 없습니다.</span>';
    return;
  }

  container.innerHTML = tags.map(([tag, count]) => `
    <span data-tag="${esc(tag)}" onclick="closeStatsModal(); searchByTag(this.dataset.tag);" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700/60 text-slate-700 dark:text-slate-200 text-xs font-semibold hover:bg-blue-600 hover:text-white transition cursor-pointer">
      <span>#${esc(tag)}</span>
      <span class="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-200 dark:bg-slate-600 text-slate-600 dark:text-slate-300">${count}</span>
    </span>
  `).join('');
}

// CSV 내보내기
function exportCSV() {
  const params = new URLSearchParams({
    firm: STATE.currentFirm,
    q: STATE.searchQuery,
    source: STATE.selectedSource,
    category: STATE.selectedCategory,
    sort: STATE.currentSort
  });
  if (STATE.isBookmarkMode) {
    // 스크랩 모아보기 중에는 다른 필터가 적용되지 않으므로 스크랩 id만 보낸다
    params.set('firm', 'all');
    params.set('q', '');
    params.set('source', '');
    params.set('category', '');
    params.set('ids', STATE.bookmarks.join(','));
  }
  window.location.href = apiUrl('export', params.toString());
  showToast('기사 목록 CSV 다운로드를 시작합니다.');
}

// 유틸리티 함수들
function showLoading(show) {
  const skeleton = document.getElementById('loadingSkeleton');
  const grid = document.getElementById('newsGrid');
  if (show) {
    skeleton.classList.remove('hidden');
    grid.classList.add('opacity-40');
  } else {
    skeleton.classList.add('hidden');
    grid.classList.remove('opacity-40');
  }
}

function formatTimeAgo(dateStr) {
  if (!dateStr) return '';
  const now = new Date();
  const date = new Date(dateStr);
  const diffMinutes = Math.floor((now - date) / (1000 * 60));

  if (diffMinutes < 1) return '방금 전';
  if (diffMinutes < 60) return `${diffMinutes}분 전`;
  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) return `${diffHours}시간 전`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays}일 전`;

  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
}

function formatAbsoluteDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toastMessage').innerText = msg;
  toast.classList.remove('translate-y-20', 'opacity-0');
  toast.classList.add('translate-y-0', 'opacity-100');

  setTimeout(() => {
    toast.classList.remove('translate-y-0', 'opacity-100');
    toast.classList.add('translate-y-20', 'opacity-0');
  }, 2800);
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ESC 키로 모달 닫기
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeArticleModal();
    closeStatsModal();
  }
});
