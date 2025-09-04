# Global Earthquake & Wildfire Dashboard

An interactive data visualization platform that tracks and analyzes global seismic activity and wildfire events in real-time, transforming raw satellite and geological data into actionable insights.

## Overview

Imagine Earth as a living, breathing system—constantly shifting, sometimes rumbling, and sometimes burning. Every day, somewhere on our planet, the ground shakes or a wildfire ignites. Our dashboard brings these events together, showing not just where and when they happen, but also their intensity and impact.

### Key Statistics (4-Month Analysis)
- **~7,000 earthquakes** recorded worldwide since January
- **~1 million wildfires** tracked globally  
- **Strongest earthquake**: Magnitude 7.7
- **Most intense wildfire**: Brightness scale >500

## Purpose

This dashboard serves multiple audiences:
- **Emergency responders** can identify where to focus resources
- **Researchers** can spot trends and correlations
- **Policymakers** can plan for high-risk zones  
- **Journalists and educators** can visualize and explain global events

## Data Sources & Technology

### Data Sources
- **NASA FIRMS**: Real-time wildfire detection from satellite imagery
- **USGS**: Global earthquake monitoring and seismic data

### Technical Implementation
- **GeoPandas**: Geospatial data processing and country mapping
- **Spatial Joins**: Converting lat/lon coordinates to country-specific data
- **Real-time Processing**: Continuous data ingestion and analysis

### Data Processing Pipeline
1. **Raw Data Collection**: Satellite and seismic data from NASA and USGS
2. **Geospatial Mapping**: Converting coordinates to country boundaries using world map shapefiles
3. **Data Enrichment**: Adding magnitude, depth, fire brightness, and confidence scores
4. **Visualization**: Interactive charts, maps, and trend analysis

## Key Features

### Global Hotspot Analysis
- Interactive world maps highlighting regions most affected by earthquakes and fires
- Country-level aggregation and ranking systems
- Real-time event tracking and historical trends

### Advanced Filtering & Analysis
- **Earthquake Analysis**: Filter by magnitude, depth, and geographic region
- **Wildfire Tracking**: Sort by brightness, radiative power, and confidence levels
- **Temporal Analysis**: 7-day moving averages and seasonal trend identification
- **Correlation Studies**: Scatter plots showing relationships between event characteristics

### Top Affected Regions
**Earthquakes**: Papua New Guinea, Indonesia, Chile  
**Wildfires**: South Sudan, India, Australia

## Insights & Applications

### Trend Analysis
- **Seismic Activity**: 7-day moving averages reveal periods of increased earthquake activity, helping identify clusters and aftershock patterns
- **Fire Patterns**: Seasonal spikes and persistent hotspots in fire-prone regions like the United States
- **Risk Assessment**: Identification of shallow, high-magnitude earthquakes that pose the greatest danger

### Decision Support
- **Emergency Response**: Real-time event mapping for resource allocation
- **Risk Planning**: Historical trend analysis for long-term preparedness
- **Research Applications**: Data-driven insights for scientific studies
- **Public Communication**: Clear visualizations for media and educational purposes

## Dashboard Interface

The dashboard provides:
- **Global Overview**: Key statistics and world maps
- **Interactive Filtering**: Zoom into specific countries, continents, or time periods
- **Trend Visualization**: Time-series charts showing activity patterns
- **Correlation Analysis**: Scatter plots revealing relationships between event characteristics
- **Real-time Updates**: Live data feeds from NASA and USGS

**Dashboard Features:**
- Real-time filtering and interactive controls
- Multi-layered map visualizations
- Statistical trend analysis
- Cross-dataset correlation plots

## Use Cases

- **Emergency Response** - Resource allocation and hotspot identification
- **Scientific Research** - Pattern analysis and correlation studies  
- **Policy Planning** - Risk assessment for high-activity regions
- **Public Education** - Accessible natural disaster awareness

## Future Enhancements

- Real-time streaming dashboard updates
- Predictive modeling for disaster forecasting
- Integration with additional data sources (weather, population density)
- Mobile-responsive interface development

### Live Dashboard : https://public.tableau.com/app/profile/anusha.kulkarni2870/viz/GlobalSeismicandFireActivityDashboard/FInalDashboard?publish=yes



*This dashboard isn't just about numbers—it's about helping people prepare, respond, and learn. It's a live story of our planet's natural events and our opportunity to respond smarter.*
