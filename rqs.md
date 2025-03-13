## **RQ1 - How is energy efficiency considered in microservice architecture research?**

How is energy consumption addressed throughout the software lifecycle and across different architectural components in microservice systems?

### **RQ1.1 - At which stages of the software lifecycle is energy efficiency considered in microservice-based systems?**

### Parameters

- **Lifecycle Stage**: Requirements, Design, Implementation, Testing, Deployment, Operations
- **Energy Awareness Stage**: Explicit requirements, Implicit concerns, Post-deployment optimization
- **Integration Approach**: Built-in, Add-on, External monitoring, Manual assessment

### **RQ1.2 - Which microservice architectural elements are primarily considered when measuring energy consumption, and how do they impact energy efficiency?**

- **Component Type**: Service units, API gateways, Message brokers, Databases, Load balancers, Service registries, Containers
- **Energy comsuption source**: Processing overhead, Communication overhead, State management, Resource allocation, Idle consumption
- **Component Relationship**: Isolated, Interconnected, Cascading effect, System-wide impact

---

## **RQ2 - How is energy consumption measured in microservices?**

### **Parameters**

### **RQ2.1 - What methods are used to measure energy consumption in microservices?**

### Parameters

- **Measurement Level**: Hardware, OS, Container, Application, Cross-cutting
- **Measurement Technique**: Static analysis, Dynamic profiling, Model-based estimation, Hybrid
- **Data Collection**: Sampling, Continuous monitoring, Event-triggered, Benchmark testing
- **Implementation Approach**: Source code instrumentation, Binary instrumentation, External monitoring

### **RQ2.2 - What tools are employed for energy consumption analysis in microservices?**

### Parameters

- **Tool Type**: Commercial, Open source, Research prototype, Custom in-house
- **Deployment Method**: Agent-based, Sidecar, External, Embedded
- **Analysis Capability**: Real-time, Historical, Predictive, Comparative
- **Granularity**: System-wide, Service-specific, Transaction-level, Code-block level

### **RQ2.3 - What energy efficiency metrics are commonly used to evaluate microservices?**

### Parameters

- **Metric Type**: Absolute (Joules, Watts), Relative (efficiency ratio), Composite
- **Measurement Scope**: CPU, Memo ry, Network, Storage, Full-stack
- **Normalization Basis**: Per request, Per transaction, Per user, Per service
- **Business Relevance**: Cost-focused, Performance-balanced, Carbon footprint

---

## **RQ3 - What architectural solutions exist for energy-efficient microservices?**

### **RQ3.1 - What approaches are used to improve energy efficiency in microservice architectures?**

- **Modernization Strategy**: Strangler pattern, Incremental refactoring, Complete rebuild, Containerization
- **Solution Category**: Architectural patterns, Design patterns, Resource management tactics, Request handling tactics, Data management tactics
- **Implementation Technologies**: Containerization, Serverless, Service mesh, Orchestration platforms, Green computing frameworks

### **RQ3.2 - What trade-offs exist between energy efficiency and other quality attributes in microservice architectures?**

### Parameters

- **Quality Attribute**: Performance, Scalability, Maintainability, Reliability, Security, Availability
- **Trade-off Relationship**: Competing, Complementary, Context-dependent, Independent
- **Trade-off Severity**: Minimal, Moderate, Significant, Prohibitive
- **Trade-off Strategy**: Architectural refactoring, Compensating tactics, Prioritization frameworks, Incremental evolution

### **RQ3.3 - What challenges affect the adoption of energy-efficient architectural solutions in microservices?**

### Parameters

- **Challenge Type**: Technical, Organizational, Knowledge-based, Economic
- **Adoption Phase**: Design-time, Implementation, Deployment, Runtime
- **Challenge Complexity**: Low, Moderate, High, Prohibitive
- **Mitigation Approach**: Tooling improvements, Knowledge sharing, Incremental adoption, Organizational change
