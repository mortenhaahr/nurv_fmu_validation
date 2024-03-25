import pickle


class Model:
    def __init__(self) -> None:
        self.cfg_desired_temperature = 35.0
        self.lid_open = False
        self.enable = True

        self.reference_to_attribute = {
            0: "cfg_desired_temperature",
            1: "ctrl_desired_temperature",
            2: "lid_open",
            3: "enable",
        }

        self._update_outputs()

    def fmi2DoStep(self, current_time, step_size, no_step_prior):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2EnterInitializationMode(self):
        return Fmi2Status.ok

    def fmi2ExitInitializationMode(self):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2SetupExperiment(self, start_time, stop_time, tolerance):
        return Fmi2Status.ok

    def fmi2SetReal(self, references, values):
        return self._set_value(references, values)

    def fmi2SetInteger(self, references, values):
        return self._set_value(references, values)

    def fmi2SetBoolean(self, references, values):
        return self._set_value(references, values)

    def fmi2SetString(self, references, values):
        return self._set_value(references, values)

    def fmi2GetReal(self, references):
        return self._get_value(references)

    def fmi2GetInteger(self, references):
        return self._get_value(references)

    def fmi2GetBoolean(self, references):
        return self._get_value(references)

    def fmi2GetString(self, references):
        return self._get_value(references)

    def fmi2Reset(self):
        return Fmi2Status.ok

    def fmi2Terminate(self):
        return Fmi2Status.ok

    def fmi2ExtSerialize(self):

        bytes = pickle.dumps(
            (
                self.cfg_desired_temperature,
                self.lid_open,
                self.enable,
            )
        )
        return Fmi2Status.ok, bytes

    def fmi2ExtDeserialize(self, bytes) -> int:
        (
            cfg_desired_temperature,
            lid_open,
            enable,
        ) = pickle.loads(bytes)
        self.cfg_desired_temperature = cfg_desired_temperature
        self.lid_open = lid_open
        self.enable = enable
        self._update_outputs()

        return Fmi2Status.ok

    def _set_value(self, references, values):

        for r, v in zip(references, values):
            setattr(self, self.reference_to_attribute[r], v)

        return Fmi2Status.ok

    def _get_value(self, references):

        values = []

        for r in references:
            values.append(getattr(self, self.reference_to_attribute[r]))

        return Fmi2Status.ok, values

    def _update_outputs(self):
        if self.enable:
            self.ctrl_desired_temperature = (
                0.6 * self.cfg_desired_temperature
                if self.lid_open
                else self.cfg_desired_temperature
            )
        else:
            self.ctrl_desired_temperature = self.cfg_desired_temperature


class Fmi2Status:
    """Represents the status of the FMU or the results of function calls.

    Values:
        * ok: all well
        * warning: an issue has arisen, but the computation can continue.
        * discard: an operation has resulted in invalid output, which must be discarded
        * error: an error has ocurred for this specific FMU instance.
        * fatal: an fatal error has ocurred which has corrupted ALL FMU instances.
        * pending: indicates that the FMu is doing work asynchronously, which can be retrived later.

    Notes:
        FMI section 2.1.3

    """

    ok = 0
    warning = 1
    discard = 2
    error = 3
    fatal = 4
    pending = 5
