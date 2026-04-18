import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GangRoom } from './gang-room';

describe('GangRoom', () => {
  let component: GangRoom;
  let fixture: ComponentFixture<GangRoom>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GangRoom]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GangRoom);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
