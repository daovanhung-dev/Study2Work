import type { StudentAccountProfileDto } from '../../models/student-profile.models';

export type StudentProfileEditDto = StudentAccountProfileDto;
export type StudentProfileEditState = 'loading' | 'ready' | 'unauthorized' | 'forbidden' | 'error';
