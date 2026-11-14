import type { StudentAccountProfileDto } from '../../models/student-profile.models';

export type StudentProfileDto = StudentAccountProfileDto;
export type StudentProfileState = 'loading' | 'ready' | 'unauthorized' | 'forbidden' | 'error';
