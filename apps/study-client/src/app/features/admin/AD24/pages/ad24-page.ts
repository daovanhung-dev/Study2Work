import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD24_SCREEN } from '../models/ad24-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad24-page',
  templateUrl: './ad24-page.html',
})
export class AD24Page {
  readonly definition = AD24_SCREEN;

  readonly metricPlaceholders = [
    { label: 'Tổng học viên tích cực', unit: 'người' },
    { label: 'Tỷ lệ hoàn thành chuyên đề', unit: '%' },
    { label: 'Giờ học tương tác cộng đồng', unit: 'giờ' },
    { label: 'Chỉ số hài lòng chung', unit: '/ 5.0' },
  ];

  readonly proposedMetrics = [
    {
      title: 'Mức độ hoạt động định kỳ (DAU/MAU)',
      description:
        'Tỷ số lượt học viên tham gia diễn đàn hỏi đáp mỗi ngày trên tổng học viên đăng ký chuyên đề.',
    },
    {
      title: 'Thời lượng tương tác với Mentor doanh nghiệp',
      description:
        'Tổng giờ thảo luận một kèm một và phản hồi được hệ thống ghi nhận có xác thực.',
    },
    {
      title: 'Tỷ lệ đáp ứng chuẩn đầu ra việc làm',
      description:
        'Tỷ lệ sinh viên tích lũy đủ chứng chỉ kỹ năng đạt ngưỡng doanh nghiệp đối tác yêu cầu.',
    },
    {
      title: 'Điểm phản hồi từ nhà tuyển dụng (NPS đối tác)',
      description:
        'Khảo sát đối tác sau 30 ngày tiếp nhận sinh viên ứng tuyển từ cổng kết nối Study2Work.',
    },
  ];

  get filterActions() {
    return this.definition.actions?.slice(0, 3) ?? [];
  }

  get exportAction() {
    return this.definition.actions?.[3] ?? null;
  }
}
