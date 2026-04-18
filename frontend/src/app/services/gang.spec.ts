import { TestBed } from '@angular/core/testing';

import { Gang } from './gang';

describe('Gang', () => {
  let service: Gang;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Gang);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
