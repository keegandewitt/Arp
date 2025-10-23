# VintageCapture VST Plugin - Development Makefile
# Simple build system for testing core components before JUCE integration

CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -I./Source
LDFLAGS =

# Targets
TEST_ANALYZER = analyzer_test

# Source files
ANALYZER_SOURCES = Source/DurationAnalyzer.cpp Source/AnalyzerTest.cpp

.PHONY: all clean test

all: $(TEST_ANALYZER)

$(TEST_ANALYZER): $(ANALYZER_SOURCES)
	@echo "Building Duration Analyzer test..."
	$(CXX) $(CXXFLAGS) $(ANALYZER_SOURCES) -o $(TEST_ANALYZER) $(LDFLAGS)
	@echo "✓ Build complete: ./$(TEST_ANALYZER)"

test: $(TEST_ANALYZER)
	@echo ""
	@echo "Running Duration Analyzer tests..."
	@echo ""
	@./$(TEST_ANALYZER)

clean:
	@echo "Cleaning build artifacts..."
	@rm -f $(TEST_ANALYZER)
	@echo "✓ Clean complete"

# Help target
help:
	@echo "VintageCapture VST Plugin - Development Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make          - Build analyzer test"
	@echo "  make test     - Build and run analyzer tests"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Components:"
	@echo "  analyzer_test - Standalone test for DurationAnalyzer"
