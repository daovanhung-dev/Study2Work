import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnDestroy, OnInit, inject } from '@angular/core';
import { Subscription } from 'rxjs';

import { AD01Metrics } from '../ui/ad01-metrics';
import { AD01Overview } from '../ui/ad01-overview';
import { AD01Shortcuts } from '../ui/ad01-shortcuts';
import { AD01Icon } from '../ui/ad01-icon';
import { AD01_SCREEN_MODEL } from '../models/ad01-screen.model';
import {
  createAD01DateRange,
  createAD01MetricCards,
  parseAD01ReportSummary,
  type AD01DateRange,
  type AD01PeriodKey,
  type AD01ReportSummary,
} from '../models/ad01-report.model';
import { AD01ReportService } from '../data-access/ad01-report.service';

@Component({
  imports: [AD01Icon, AD01Metrics, AD01Overview, AD01Shortcuts],
  selector: 'study-ad01-page',
  styleUrl: './ad01-page.css',
  templateUrl: './ad01-page.html',
})
export class AD01Page implements OnInit, OnDestroy {
  private readonly reportService = inject(AD01ReportService);
  private readonly changeDetector = inject(ChangeDetectorRef);
  private reportRequest: Subscription | null = null;

  readonly screenModel = AD01_SCREEN_MODEL;
  readonly periods = [
    { key: 'today', label: 'Hôm nay' },
    { key: 'last7', label: '7 ngày qua' },
    { key: 'last30', label: '30 ngày qua' },
  ] as const;
  selectedPeriod: AD01PeriodKey = 'last30';
  selectedRange: AD01DateRange = createAD01DateRange(this.selectedPeriod);
  status: 'loading' | 'ready' | 'error' = 'loading';
  errorMessage = '';
  report: AD01ReportSummary | null = null;
  metrics = createAD01MetricCards();

  ngOnInit(): void {
    this.loadReport();
  }

  ngOnDestroy(): void {
    this.reportRequest?.unsubscribe();
  }

  selectPeriod(period: AD01PeriodKey): void {
    this.selectedPeriod = period;
    this.loadReport();
  }

  refresh(): void {
    this.loadReport();
  }

  private loadReport(): void {
    // Hủy request cũ để phản hồi kỳ trước không ghi đè kỳ đang chọn.
    this.reportRequest?.unsubscribe();
    this.selectedRange = createAD01DateRange(this.selectedPeriod);
    this.report = null;
    this.metrics = createAD01MetricCards();
    this.errorMessage = '';
    this.status = 'loading';

    // Tải report qua service màn hình, luôn gửi đủ hai ngày inclusive.
    this.reportRequest = this.reportService.getSummary(this.selectedRange).subscribe({
      next: (envelope) => {
        const report = parseAD01ReportSummary(envelope, this.selectedRange);
        if (report === null) {
          this.showError('Phản hồi số liệu không đúng định dạng báo cáo.');
          return;
        }
        this.report = report;
        this.metrics = createAD01MetricCards(report.metrics);
        this.status = 'ready';
        this.changeDetector.markForCheck();
      },
      error: (error: unknown) => this.showError(this.messageFor(error)),
    });
  }

  private messageFor(error: unknown): string {
    if (error instanceof HttpErrorResponse && error.status === 401) {
      return 'Phiên Admin không còn hợp lệ. Vui lòng đăng nhập lại.';
    }
    if (error instanceof HttpErrorResponse && error.status === 403) {
      return 'Phiên Admin không có quyền xem báo cáo.';
    }
    return 'Không thể tải số liệu. Hãy kiểm tra kết nối rồi thử lại.';
  }

  private showError(message: string): void {
    this.errorMessage = message;
    this.status = 'error';
    this.changeDetector.markForCheck();
  }
}
