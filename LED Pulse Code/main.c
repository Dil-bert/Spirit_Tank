/*
 * SpiritTank_LED_BLINK.c
 *
 * Created: 7/14/2020 9:38:17 AM
 * Author : gausp
 */ 

/*
 * Timer 1 is used to have a period of 10.01ms (~99.89Hz) with an on time of 10us and an off time of 10ms.
 * Timer 1 is set to a fast PWM mode and OC1A (PORTB1) is set to clear on compare match (low level).
 * The signal is enabled when PINB2 receives a signal. When enabled, a forwarding signal is generated on PINB0.
 */
#define F_CPU 16000000UL
#include <avr/io.h>

int checkStopCond();
void gpioInit();
void timer1Init();

int main(void)
{
	
	gpioInit();
	timer1Init();
	
	while (1)
	{
		if( checkStopCond() ) {
			TCCR1B &= ~(1 << CS11);
			PORTB &= ~(1 << PORTB0);
			// STOP the timer 
		}
		else {
			TCCR1B |= (1 << CS11);
			PORTB |= (1 << PORTB0);
			// STARTS timer if it was paused
		}
	}
}


int checkStopCond() {
	//When a button is pushed, the stop condition is met. This would be changed so that a signal can be received from the raspberry pi to stop the PWM.
	if(!(PINB & (1 << PINB2)))
		return 1;
	else
		return 0;
}

void gpioInit() {
	DDRB |= (1 << DDB0) | (1 << DDB1);
	// PORTB0 and PORTB1 are set as outputs.
	
	DDRB &= ~(1 << DDB2);
	PORTB |= (1 << PORTB2);
	// PORTB2 set as input and pull-up is enabled.
	
}

void timer1Init() {
	ICR1 = 20019;
	// set TOP to 16bit (period of 10.01ms, frequency ~99.89Hz)

	OCR1A = 19999;
	// set off time for 10ms leaving on time for 10us

	TCCR1A |= (1 << COM1A1)|(1 << COM1A0);
	// Clear OC1A on Compare Match (Set output to low level)

	TCCR1A |= (1 << WGM11);
	TCCR1B |= (1 << WGM12)|(1 << WGM13);
	// Mode 14, set Fast PWM mode using ICR1 as TOP
	    
	TCCR1B |= (1 << CS11);
	// START the timer with prescaler of 8
}