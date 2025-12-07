🧪 Bio-Scrubber

A modular Python simulation toolkit for modeling algae-based CO₂ capture systems

Bio-Scrubber is a professional, test-supported Python project that models biomass production and CO₂ sequestration using algae-based photobioreactors.
It is designed for researchers, climate technologists, hobbyists, and engineers exploring carbon-offset strategies such as backyard bioreactors, ocean-based farms, or lifted systems with additional energy sources.

The system is built with clarity, modularity, and extensibility in mind — making it suitable for real scientific work and as a polished portfolio piece.

🚀 Features

Modular Simulation Engine
Easily configure reactors, bioreactor farms, or planetary-scale deployments.

Flexible Reactor Parameters
Customize surface area, light availability, uptime, productivity, CO₂ conversion ratio, and more.

Energy Modeling (optional)
Integrates clean-energy sources such as:

Wave-powered generators

Solar / LED nighttime illumination

Lift systems (balloon-supported net arrays)

Batch Scenarios
Run realistic, optimistic, pessimistic, or custom scenarios across millions of household-equivalent reactors.

Command-Line Interface
python3 cli.py --scenario realistic_medium --households 10000000

Unit-tested Codebase
Includes a full tests/ suite built with pytest to validate models, equations, and CLI behavior.

Professional Project Layout
Following modern Python standards:

bioscrubber/
  ├── src/
  │   ├── bioscrubber/
  │   │   ├── models/
  │   │   ├── scenarios/
  │   │   ├── energy/
  │   │   └── cli.py
  ├── tests/
  ├── pyproject.toml
  ├── README.md
  └── ...

🧬 How the Model Works

Each simulated reactor calculates:

Daily biomass production

CO₂ captured per gram of biomass

Annual performance with uptime factored in

Scaling performance across multiple reactors or households

Example per-reactor output:

Reactor parameters:
  Area:              4.00 m²
  Productivity:      20.0 g/m²/day
  CO₂ per biomass:   1.80 g CO₂ / g biomass
  Uptime:            80.0 %

Per household / reactor:
  CO₂ removed:       42.05 kg / year


The simulation also supports extended models such as:

Lifted night-cycle arrays for increased surface absorption

LED-supplemented 24/7 growth

Wave-generated power buffers

📦 Installation
git clone https://github.com/yourusername/bioscrubber
cd bioscrubber
pip install -e .


Or if using uv:

uv run python3 cli.py

▶️ Running a Simulation
Predefined Scenarios
python3 cli.py --scenario realistic_medium --households 1000000

Custom Parameters
python3 cli.py \
  --area 5.0 \
  --productivity 25 \
  --uptime 0.9 \
  --co2-per-gram 1.8 \
  --households 50000

Energy-Augmented Mode
python3 cli.py --scenario lifted_led_wave --households 20000000

🧪 Running Tests
pytest -v


Test suite includes:

Reactor model validation

Energy-generation modules

Scenario computations

CLI behavior and error handling

📘 Roadmap

Integrate ocean-current drift maps

Add reinforcement-learning optimization for panel placement

Add graphical dashboard for scenario visualization

Export full simulation reports as JSON or CSV

Build scientific paper–ready charts

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue to discuss what you'd like to add.

📄 License

MIT License. See LICENSE for details.
