class SummaryTable {
  constructor() {
    this.stocks = [];
    this.filteredStocks = [];
    this.currentFilters = {
      priority: 'all',
      search: ''
    };
    this.sortColumn = 'priority';
    this.sortDirection = 'asc';
    
    this.init();
  }

  init() {
    this.parseStockData();
    this.setupEventListeners();
    this.applyFilters();
  }

  parseStockData() {
    const table = document.querySelector('.summary-table');
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 6) {
        const priorityCell = cells[5];
        const badges = priorityCell.querySelectorAll('.priority-badge');
        const priorities = [];
        const hasObserve = false;
        
        badges.forEach(badge => {
          if (badge.classList.contains('high')) {
            priorities.push('high');
          } else if (badge.classList.contains('medium')) {
            priorities.push('medium');
          } else if (badge.classList.contains('low')) {
            priorities.push('low');
          }
          if (badge.classList.contains('observe')) {
            priorities.push('observe');
          }
        });

        const stock = {
          id: index,
          code: cells[0]?.textContent?.trim() || '',
          name: cells[1]?.textContent?.trim() || '',
          currentPrice: this.parsePrice(cells[2]?.textContent?.trim() || '0'),
          targetPrice: this.parseTargetPrice(cells[3]?.textContent?.trim() || '0'),
          recommendation: cells[4]?.textContent?.trim() || '',
          priorities: priorities,
          primaryPriority: this.getPrimaryPriority(priorities),
          row: row,
          html: row.innerHTML
        };
        this.stocks.push(stock);
      }
    });
    
    this.filteredStocks = [...this.stocks];
  }

  getPrimaryPriority(priorities) {
    if (priorities.includes('high')) return 'high';
    if (priorities.includes('medium')) return 'medium';
    if (priorities.includes('low')) return 'low';
    return 'medium';
  }

  parsePrice(text) {
    const match = text.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  parseTargetPrice(text) {
    const matches = text.match(/[\d.]+/g);
    if (!matches || matches.length === 0) return 0;
    if (matches.length === 1) return parseFloat(matches[0]);
    const avg = matches.reduce((sum, m) => sum + parseFloat(m), 0) / matches.length;
    return avg;
  }

  setupEventListeners() {
    const filterBtns = document.querySelectorAll('.filter-btn[data-filter="priority"]');
    filterBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const group = e.target.closest('.filter-buttons');
        if (group) {
          group.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
          
          const filterValue = e.target.dataset.value;
          this.currentFilters.priority = filterValue;
          this.applyFilters();
        }
      });
    });

    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.currentFilters.search = e.target.value.toLowerCase();
        this.applyFilters();
      });
    }

    const tableHeaders = document.querySelectorAll('.summary-table th[data-sortable="true"]');
    tableHeaders.forEach(header => {
      header.addEventListener('click', () => {
        const column = header.dataset.column;
        if (this.sortColumn === column) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortColumn = column;
          this.sortDirection = 'asc';
        }
        this.applyFilters();
        this.updateSortIndicators();
      });
    });
  }

  applyFilters() {
    this.filteredStocks = this.stocks.filter(stock => {
      if (this.currentFilters.priority !== 'all') {
        if (!stock.priorities.includes(this.currentFilters.priority)) {
          return false;
        }
      }
      if (this.currentFilters.search) {
        const searchStr = `${stock.code} ${stock.name}`.toLowerCase();
        if (!searchStr.includes(this.currentFilters.search)) {
          return false;
        }
      }
      return true;
    });

    this.sortStocks();
    this.updateTable();
    this.updateCount();
  }

  sortStocks() {
    this.filteredStocks.sort((a, b) => {
      let comparison = 0;
      
      switch (this.sortColumn) {
        case 'code':
          comparison = a.code.localeCompare(b.code);
          break;
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'currentPrice':
          comparison = a.currentPrice - b.currentPrice;
          break;
        case 'targetPrice':
          comparison = a.targetPrice - b.targetPrice;
          break;
        case 'priority':
          const priorityOrder = { high: 0, medium: 1, low: 2 };
          comparison = priorityOrder[a.primaryPriority] - priorityOrder[b.primaryPriority];
          break;
        default:
          comparison = 0;
      }

      return this.sortDirection === 'asc' ? comparison : -comparison;
    });
  }

  updateTable() {
    const tbody = document.querySelector('.summary-table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (this.filteredStocks.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td colspan="6" class="no-results">
          <div class="no-results-icon">🔍</div>
          <div class="no-results-text">没有找到符合条件的股票</div>
        </td>
      `;
      tbody.appendChild(row);
      return;
    }

    this.filteredStocks.forEach(stock => {
      const row = document.createElement('tr');
      row.innerHTML = stock.html;
      tbody.appendChild(row);
    });
  }

  updateCount() {
    const countEl = document.querySelector('.summary-table-count');
    if (countEl) {
      countEl.textContent = `${this.filteredStocks.length} / ${this.stocks.length} 只股票`;
    }
  }

  updateSortIndicators() {
    const headers = document.querySelectorAll('.summary-table th[data-sortable="true"]');
    headers.forEach(header => {
      header.classList.remove('sorted-asc', 'sorted-desc');
      if (header.dataset.column === this.sortColumn) {
        header.classList.add(this.sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc');
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new SummaryTable();
});
