import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Gangs } from './gangs';

describe('Gangs', () => {
  let component: Gangs;
  let fixture: ComponentFixture<Gangs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Gangs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Gangs);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
