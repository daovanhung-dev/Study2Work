import 'package:flutter/material.dart';

class Project {
  final String id;
  final String name;
  Project(this.id, this.name);
}

class Job {
  final String id;
  final String projectId;
  final String title;
  final List<String> requiredSkills;
  final int minExp;
  Job({required this.id, required this.projectId, required this.title, required this.requiredSkills, required this.minExp});
}

class CV {
  final String name;
  final List<String> skills;
  final int exp;
  final String status;
  final String jobId;
  CV({required this.name, required this.skills, required this.exp, required this.status, required this.jobId});
}

class LocCV extends StatefulWidget {
  const LocCV({super.key});

  @override
  State<LocCV> createState() => _LocCVState();
}

class _LocCVState extends State<LocCV> {
  final List<Project> _projects = [
    Project('p1', 'ERP Upgrade'),
    Project('p2', 'E-Commerce App'),
    Project('p3', 'AI Resume Screener'),
  ];

  late final List<Job> _jobs = [
    Job(id: 'j1', projectId: 'p1', title: 'Backend Engineer', requiredSkills: ['Java', 'Spring', 'SQL'], minExp: 2),
    Job(id: 'j2', projectId: 'p1', title: 'QA Engineer', requiredSkills: ['Testing', 'Selenium'], minExp: 1),
    Job(id: 'j3', projectId: 'p2', title: 'Flutter Developer', requiredSkills: ['Flutter', 'Dart', 'REST'], minExp: 1),
    Job(id: 'j4', projectId: 'p2', title: 'UI/UX Designer', requiredSkills: ['Figma', 'UI', 'UX'], minExp: 2),
    Job(id: 'j5', projectId: 'p3', title: 'ML Engineer', requiredSkills: ['Python', 'NLP', 'TensorFlow'], minExp: 2),
  ];

  late final List<CV> _cvs = [
    CV(name: 'Nguyễn Văn A', skills: ['Java', 'Spring', 'SQL'], exp: 3, status: 'Applied', jobId: 'j1'),
    CV(name: 'Trần Thị B', skills: ['Flutter', 'Dart', 'REST'], exp: 2, status: 'Interview', jobId: 'j3'),
    CV(name: 'Lê Văn C', skills: ['Python', 'NLP', 'TensorFlow'], exp: 2, status: 'Screened', jobId: 'j5'),
    CV(name: 'Phạm Thị D', skills: ['Testing', 'Selenium'], exp: 1, status: 'Offered', jobId: 'j2'),
    CV(name: 'Đỗ Quốc E', skills: ['Figma', 'UI', 'UX'], exp: 3, status: 'Hired', jobId: 'j4'),
    CV(name: 'Vũ Minh F', skills: ['Flutter', 'REST'], exp: 1, status: 'Rejected', jobId: 'j3'),
  ];

  String? _selectedProjectId;
  String? _selectedJobId;
  String _selectedStatus = 'Tất cả';
  final List<String> _allSkills = ['Java','Spring','SQL','Testing','Selenium','Flutter','Dart','REST','Figma','UI','UX','Python','NLP','TensorFlow'];
  final Set<String> _selectedSkills = {};
  int? _minExp;

  bool _filtered = false;
  List<CV> _results = [];

  List<Job> get _jobsByProject {
    if (_selectedProjectId == null) return _jobs;
    return _jobs.where((j) => j.projectId == _selectedProjectId).toList();
  }

  void _applyFilter() {
    setState(() {
      _filtered = true;
      _results = _cvs.where((cv) {
        final job = _jobs.firstWhere((j) => j.id == cv.jobId);
        final projectOk = _selectedProjectId == null || job.projectId == _selectedProjectId;
        final jobOk = _selectedJobId == null || cv.jobId == _selectedJobId;
        final statusOk = _selectedStatus == 'Tất cả' || cv.status == _selectedStatus;
        final expOk = _minExp == null || cv.exp >= _minExp!;
        final skillsOk = _selectedSkills.isEmpty || _selectedSkills.every((s) => cv.skills.contains(s));
        return projectOk && jobOk && statusOk && expOk && skillsOk;
      }).toList();
    });
  }

  void _clearFilter() {
    setState(() {
      _selectedProjectId = null;
      _selectedJobId = null;
      _selectedStatus = 'Tất cả';
      _selectedSkills.clear();
      _minExp = null;
      _filtered = false;
      _results.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Positioned.fill(child: Image.asset('assets/bg_trangchu.jpg', fit: BoxFit.cover)),
        Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            backgroundColor: const Color(0xFF3F51B5),
            foregroundColor: Colors.white,
            title: const Text('Lọc CV'),
            elevation: 0,
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 720),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Wrap(
                      spacing: 12,
                      runSpacing: 12,
                      children: [
                        _buildProjectDropdown(),
                        _buildJobDropdown(),
                        _buildStatusDropdown(),
                        _buildMinExpField(),
                        _buildSkillPicker(context),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF3F51B5),
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          onPressed: _applyFilter,
                          icon: const Icon(Icons.filter_alt),
                          label: const Text('Lọc CV'),
                        ),
                        const SizedBox(width: 12),
                        OutlinedButton.icon(
                          onPressed: _clearFilter,
                          icon: const Icon(Icons.refresh),
                          label: const Text('Đặt lại'),
                        ),
                      ],
                    ),
                    const SizedBox(height: 18),
                    const Text('Kết quả:', style: TextStyle(fontWeight: FontWeight.w600)),
                    const SizedBox(height: 8),
                    if (!_filtered)
                      const Text('Chọn điều kiện rồi bấm Lọc CV nha.', style: TextStyle(color: Colors.black54))
                    else if (_results.isEmpty)
                      const Text('Không tìm thấy CV phù hợp.', style: TextStyle(color: Colors.black45))
                    else
                      ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: _results.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 8),
                        itemBuilder: (context, i) {
                          final cv = _results[i];
                          final job = _jobs.firstWhere((j) => j.id == cv.jobId);
                          final project = _projects.firstWhere((p) => p.id == job.projectId);
                          return Card(
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            child: ListTile(
                              leading: const CircleAvatar(child: Icon(Icons.person)),
                              title: Text(cv.name),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text('Dự án: ${project.name} • Job: ${job.title} • Trạng thái: ${cv.status}'),
                                  const SizedBox(height: 4),
                                  Wrap(
                                    spacing: 6,
                                    runSpacing: -8,
                                    children: cv.skills.map((s) => Chip(label: Text(s))).toList(),
                                  ),
                                  const SizedBox(height: 4),
                                  Text('Kinh nghiệm: ${cv.exp} năm'),
                                ],
                              ),
                              trailing: const Icon(Icons.chevron_right),
                            ),
                          );
                        },
                      ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  // --- filter widgets ---
  Widget _buildProjectDropdown() {
    return SizedBox(
      width: 260,
      child: DropdownButtonFormField<String?>(
        value: _selectedProjectId,
        items: [
          const DropdownMenuItem<String?>(value: null, child: Text('Tất cả dự án')),
          ..._projects.map((p) => DropdownMenuItem<String?>(value: p.id, child: Text(p.name)))
        ],
        onChanged: (v) => setState(() { _selectedProjectId = v; _selectedJobId = null; }),
        decoration: const InputDecoration(prefixIcon: Icon(Icons.folder_open), labelText: 'Dự án'),
      ),
    );
  }

  Widget _buildJobDropdown() {
    final jobs = _jobsByProject;
    return SizedBox(
      width: 260,
      child: DropdownButtonFormField<String?>(
        value: _selectedJobId,
        items: [
          const DropdownMenuItem<String?>(value: null, child: Text('Tất cả job')),
          ...jobs.map((j) => DropdownMenuItem<String?>(value: j.id, child: Text(j.title)))
        ],
        onChanged: (v) => setState(() => _selectedJobId = v),
        decoration: const InputDecoration(prefixIcon: Icon(Icons.work_outline), labelText: 'Job'),
      ),
    );
  }

  Widget _buildStatusDropdown() {
    const statuses = ['Tất cả','Applied','Screened','Interview','Offered','Hired','Rejected'];
    return SizedBox(
      width: 220,
      child: DropdownButtonFormField<String>(
        value: _selectedStatus,
        items: statuses.map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
        onChanged: (v) => setState(() => _selectedStatus = v ?? 'Tất cả'),
        decoration: const InputDecoration(prefixIcon: Icon(Icons.flag_circle_outlined), labelText: 'Trạng thái CV'),
      ),
    );
  }

  Widget _buildMinExpField() {
    return SizedBox(
      width: 220,
      child: TextFormField(
        keyboardType: TextInputType.number,
        decoration: const InputDecoration(
          labelText: 'Kinh nghiệm tối thiểu (năm)',
          prefixIcon: Icon(Icons.timeline),
        ),
        onChanged: (v) => setState(() => _minExp = int.tryParse(v)),
      ),
    );
  }

  Widget _buildSkillPicker(BuildContext context) {
    return SizedBox(
      width: 720,
      child: InkWell(
        onTap: () async {
          final selected = await showDialog<Set<String>>(
            context: context,
            builder: (_) => _SkillDialog(all: _allSkills, chosen: _selectedSkills),
          );
          if (selected != null) {
            setState(() {
              _selectedSkills
                ..clear()
                ..addAll(selected);
            });
          }
        },
        child: InputDecorator(
          decoration: const InputDecoration(
            labelText: 'Kỹ năng (chọn nhiều)',
            prefixIcon: Icon(Icons.code),
            border: OutlineInputBorder(),
          ),
          child: _selectedSkills.isEmpty
              ? const Text('— chưa chọn —', style: TextStyle(color: Colors.black45))
              : Wrap(spacing: 6, children: _selectedSkills.map((s) => Chip(label: Text(s))).toList()),
        ),
      ),
    );
  }
}

class _SkillDialog extends StatefulWidget {
  const _SkillDialog({required this.all, required this.chosen});
  final List<String> all;
  final Set<String> chosen;

  @override
  State<_SkillDialog> createState() => _SkillDialogState();
}

class _SkillDialogState extends State<_SkillDialog> {
  late final Set<String> _temp = {...widget.chosen};

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Chọn kỹ năng'),
      content: SizedBox(
        width: 420,
        child: SingleChildScrollView(
          child: Column(
            children: widget.all.map((s) {
              final checked = _temp.contains(s);
              return CheckboxListTile(
                value: checked,
                onChanged: (v) => setState(() { if (v == true) _temp.add(s); else _temp.remove(s); }),
                title: Text(s),
                dense: true,
                controlAffinity: ListTileControlAffinity.leading,
              );
            }).toList(),
          ),
        ),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Huỷ')),
        ElevatedButton(onPressed: () => Navigator.pop(context, _temp), child: const Text('Xong')),
      ],
    );
  }
}