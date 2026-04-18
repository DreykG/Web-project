import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Case, CaseItem, CaseOpening, LiveDrop } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class CaseService {
  private apiUrl = 'http://localhost:8000/api/cases/git';

  constructor(private http: HttpClient) {}

  
}
