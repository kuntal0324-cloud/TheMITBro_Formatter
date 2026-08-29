from src.universal_visual_intelligence import understand_visual
def test_phasor():
 v=understand_visual("Draw phasor diagram V=220∠30 and I=10∠-20.")
 assert len(v.entities)==2 and v.entities[0].properties["angle_deg"]==30
def test_control_feedback():
 v=understand_visual("Draw feedback control system block diagram where G(s)=10/(s+1), H(s)=1.")
 assert v.properties["feedback"] and any(x.kind=="feedback" for x in v.relations)
def test_pwm():
 v=understand_visual("Sketch PWM waveform with 40 percent duty cycle at 10 kHz.")
 assert v.properties["duty_cycle_percent"]==40
