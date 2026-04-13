import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradeRoom } from './trade-room';

describe('TradeRoom', () => {
  let component: TradeRoom;
  let fixture: ComponentFixture<TradeRoom>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TradeRoom]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TradeRoom);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
