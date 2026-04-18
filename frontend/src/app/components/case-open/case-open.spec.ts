import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CaseOpen } from './case-open';

describe('CaseOpen', () => {
  let component: CaseOpen;
  let fixture: ComponentFixture<CaseOpen>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CaseOpen]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CaseOpen);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
