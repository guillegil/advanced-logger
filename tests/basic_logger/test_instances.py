
from advanced_logger import AdvancedLogger

class TestAdvancedLoggerSingleton:
    """Test suite for AdvancedLogger singleton behavior"""

    def setup_method(self):
        """Clear singleton instances before each test"""
        AdvancedLogger._instances.clear()

    def test_same_name_returns_same_instance(self):
        """Test that creating loggers with the same name returns the same object"""
        log1 = AdvancedLogger('test_logger')
        log2 = AdvancedLogger('test_logger')

        # -- ✅ Should be the exact same object -------------------------- #
        assert log1 is log2
        assert id(log1) == id(log2)

    def test_different_names_return_different_instances(self):
        """Test that different logger names create different instances"""
        log1 = AdvancedLogger('logger1')
        log2 = AdvancedLogger('logger2')

        # -- ✅ Should be different objects ------------------------------ #
        assert log1 is not log2
        assert id(log1) != id(log2)

    def test_handler_management_across_same_instances(self):
        """Test that handler management works across same-name instances"""
        log1 = AdvancedLogger('shared_logger')
        log2 = AdvancedLogger('shared_logger')

        # -- Add handler through first instance --------------------------- #
        log1.init_term_handler('test_handler', level='info')

        # -- ✅ Verify handler exists in both (since they're the same object)
        assert 'test_handler' in log1.active_handlers
        assert 'test_handler' in log2.active_handlers

        # -- Remove handler through second instance -------------------- #
        log2.remove_handler('test_handler')

        # -- ✅ Verify handler is removed from both ----------------------- #
        assert 'test_handler' not in log1.active_handlers
        assert 'test_handler' not in log2.active_handlers

    def test_step_counter_consistency(self):
        """Test that step counters are shared across same-name instances"""
        log1 = AdvancedLogger('step_logger')
        log2 = AdvancedLogger('step_logger')

        # -- ✅ Initial state --------------------------------- #
        assert log1.stepn == 0
        assert log2.stepn == 0

        # -- ✅ Step through first instance ------------------- #
        log1.step("Step 1")
        assert log1.stepn == 1
        assert log2.stepn == 1  # Should be same since same object

        # -- ✅ Step through second instance ------------------ #
        log2.step("Step 2")
        assert log1.stepn == 2
        assert log2.stepn == 2

    def test_substep_counter_consistency(self):
        """Test that substep counters are shared across same-name instances"""
        log1 = AdvancedLogger('substep_logger')
        log2 = AdvancedLogger('substep_logger')

        # -- Create a step first -------------------------------- #
        log1.step("Main step")

        # -- ✅ Add substeps through different instances -------- #
        log1.substep("Substep 1")
        assert log1.substepn == 1
        assert log2.substepn == 1

        # -- ✅ Add substeps through different instances -------- #
        log2.substep("Substep 2")
        assert log1.substepn == 2
        assert log2.substepn == 2

    def test_test_procedure_consistency(self):
        """Test that test procedure is shared across same-name instances"""
        log1 = AdvancedLogger('procedure_logger')
        log2 = AdvancedLogger('procedure_logger')

        # Add steps through different instances
        log1.step("Step from log1")
        log2.step("Step from log2")

        # Both should have the same procedure
        assert len(log1.test_procedure['steps']) == 2
        assert len(log2.test_procedure['steps']) == 2
        assert log1.test_procedure is log2.test_procedure

    def test_init_not_called_multiple_times(self):
        """Test that __init__ is not called multiple times for same instance"""
        log1 = AdvancedLogger('init_test', init_default_term_handler=True)

        # Should have one handler
        initial_handler_count = len(log1.active_handlers)

        # Create "another" instance with same name
        log2 = AdvancedLogger('init_test', init_default_term_handler=True)

        # Should still be the same object with same handler count
        assert log1 is log2
        assert len(log2.active_handlers) == initial_handler_count

    def test_reset_steps_affects_all_instances(self):
        """Test that reset_steps affects all instances with same name"""
        log1 = AdvancedLogger('reset_logger')
        log2 = AdvancedLogger('reset_logger')

        # -- Add some steps --------------------------------- #
        log1.step("Step 1")
        log2.substep("Substep 1")

        # -- ✅ Check step count ---------------------------- #
        assert log1.stepn == 1
        assert log2.substepn == 1

        # -- Reset through one instance -------------------- #
        log1.reset_steps()

        # -- ✅ Both should be reset ----------------------- #
        assert log1.stepn == 0
        assert log2.stepn == 0
        assert log1.substepn == 0
        assert log2.substepn == 0

    def test_multiple_different_loggers_independence(self):
        """Test that different logger names maintain independence"""
        log_a1 = AdvancedLogger('logger_a')
        log_a2 = AdvancedLogger('logger_a')
        log_b1 = AdvancedLogger('logger_b')
        log_b2 = AdvancedLogger('logger_b')

        # -- ✅ Same names should be same objects -------------------- #
        assert log_a1 is log_a2
        assert log_b1 is log_b2

        # -- ✅ Different names should be different objects ---------- #
        assert log_a1 is not log_b1
        assert log_a2 is not log_b2

        # -- ✅ Steps should be independent -------------------------- #
        log_a1.step("Step A")
        log_b1.step("Step B1")
        log_b1.step("Step B2")

        assert log_a1.stepn == 1
        assert log_a2.stepn == 1  # Same as log_a1
        assert log_b1.stepn == 2
        assert log_b2.stepn == 2  # Same as log_b1

    def test_instances_dict_tracking(self):
        """Test that _instances dict correctly tracks created loggers"""
        # -- Clear instances ---------------------------------- #
        AdvancedLogger._instances.clear()

        # -- ✅ Initially empty ------------------------------- #
        assert len(AdvancedLogger._instances) == 0

        # -- ✅ Create first logger --------------------------- #
        log1 = AdvancedLogger('tracked_logger')
        assert len(AdvancedLogger._instances) == 1
        assert 'tracked_logger' in AdvancedLogger._instances

        # -- ✅ Create "second" logger with same name --------- #
        log2 = AdvancedLogger('tracked_logger')
        assert len(AdvancedLogger._instances) == 1  # Still just one
        assert log1 is log2

        # -- ✅ Create different logger ----------------------- #
        log3 = AdvancedLogger('another_logger')
        assert len(AdvancedLogger._instances) == 2
        assert 'another_logger' in AdvancedLogger._instances
