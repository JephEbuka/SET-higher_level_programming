#!/usr/bin/env python3
"""Install or update the AirBnB clone models, console and unit tests.

Usage:
    python3 setup_airbnb.py --author "Full Name <email@example.com>"
    python3 setup_airbnb.py --target . --update

The embedded ZIP is identical to AirBnB_clone.zip. Updating an existing
project backs up replaced files beside the project directory. Git metadata,
saved file.json data and unrelated files are never included in the update.
"""

import argparse
import base64
from datetime import datetime
import io
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
import zipfile


PAYLOAD = (
    "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"
    "ne7oo+WtLweAJUffsvQTCY91R+dTzIrPQoYDAMC8kQi+in/54+sdsEz59OGUWTgoUuug"
    "YNGpYKJ8UFFSbpWHUePoLD6KXEkgzy39AFBLAwQUAAAACACKUSddqhR08UgAAABHAAAA"
    "JgAAAEFpckJuQl9jbG9uZS9tb2RlbHMvZW5naW5lL19faW5pdF9fLnB5U1bULy0u0k/K"
    "zNMvqCzJyM8z5lJSUgooyi/LTElVKC7JL0pMT1VIzUvPzEstVkjLL1IoyUhVcMwscspz"
    "UkjOyc9L1QOq5wIAUEsDBBQAAAAIAFhdJ122HAXG7AIAAHYHAAAqAAAAQWlyQm5CX2Ns"
    "b25lL21vZGVscy9lbmdpbmUvZmlsZV9zdG9yYWdlLnB5lVVNb9swDL37V3DuxSky97DL"
    "0CGHfRXohnVDg2GHojAUm07V2pIhycmyIv99pOSPOEgHzBdZJvX4+ETSZ68uWmsuVlJd"
    "NDv3oNWbKI7jJRopKvkHodYFViCVdULlaMFp+LL8fgNCFWDQOm0Q3APWUBpdQyHtU0rn"
    "o0jWjTYOHq1WURTllbAWrmSFSzoh1ngZAT3k+RWxIaC1tA4NFqBXj5g7SxGhxlqbnY/U"
    "oLHkESKRqSSklLFDMMbKMv6YNcI9wALiwSPurD3wAp734USBJYiqSixW5SwQ6kjdomuN"
    "4mhQyQ1SWrmTWglio8tDtoMunkePYMJxxk2HwGNMhVsfc87JHgcO0JT0gA2tlWoNkrgH"
    "GZWo0aty/QmE9YYn3E0Y0J5FeN6nz/s4LbWphUvcrsGEQxIpxsgyzyCVxWw4OOV8Rzj3"
    "BETbkb4VGzyh2S8jHbKeJ/VhoiJUTsCe0C2EE3wxFO7SU3I6Y82TGRB3zsYz5ZufEkwp"
    "Zm2T2X6A2kq6f92gSjrPoSrmEG/jOaDKdUGCLuLWla/fxjOmZp1BUY/58OPLq2jrJmF6"
    "885nNgphsNKiOFk+oS9YDNs23AikRegkf4Vo34FcK+8DtbT+gn3FHqrizG7K6J+5mf/J"
    "7UB0n2ZIpEuwd8DfOTbOd+2Ndle6VcVnY7SZQoVij4ZvZ3AdWl+UXMg+a5va0PaESaXh"
    "p4jYaFlALk3eVsJAmBc2HXD8POlOU7Eq6XadE7wP25OuK2Ex64ZW8P5AX77xh5P++QHu"
    "x5dAm0pQH3ZeP3hz0s3gRuK297v1u5OO1BRuwFvy5qRba7EXBn7S+yhyV0XcM5PLiIdk"
    "48sx8fnUh6HIzMuRxadGJr8e2TxNsvn1yMbCkYmXI0t3VWTs3o7sQSQyh5fROnZ095cp"
    "wuQedOrngnDOyFXr0P8zuKj7oTCtU69pFiboohfwbjx9F2fBmmXx/f1RiQcG/Tg8gErO"
    "z0eIl8Zo2jbEC5MeZxb9BVBLAwQUAAAACABVXSddKoVwVecAAACkAQAAHAAAAEFpckJu"
    "Ql9jbG9uZS9tb2RlbHMvcGxhY2UucHldj09rwzAMxe/+FFp22WAkhd0Gu4xeB2PXMoLi"
    "qIkg/oOlQPPtZyejWeuT9JP0nt/jQzNLajr2TVx0DP7VVFV1pDN7Ah0J0NrgXOhROXjI"
    "BU113jDmnILbeqk7FGrXGtjFkBQ+MvkswBhjJxSBrwktPV3585uB/LLUN8VEQl4B/Z0d"
    "+h5YBaZgV/ACFiNa1mUdoSPPyiTbj4pembXcw3tWXsEslG6Az1d715PYxHF121dm1+Wr"
    "FIKTTA//YYc63g4cXtphJtEriYkttd3Seh7GHU85g859cT/Ufyj44Z5tqUqK4nH6Mb9Q"
    "SwMEFAAAAAgAV10nXdQWeJifAAAA6QAAAB0AAABBaXJCbkJfY2xvbmUvbW9kZWxzL3Jl"
    "dmlldy5weVWOvQ6CUAxG9/sUFQd1gcHNxMW4uvACpFxKaML9yW0RfXsvEE3s1O98yWn3"
    "u2qSVLXsq/jWIfizKYriTj17Ah0IEj2ZZnCho7HMlTF9Cm7LUrYo1Kw7sIshKdwyeSzA"
    "GGNHFIF6NRx/xeliIE921RQTCXkFhEkoHQTmxKrkv2dDD+gBrQ0uX0Hl4LcnFkMc0VLD"
    "HVyzbCWL5A8ovXRLH1BLAwQUAAAACABWXSddBUeGcHsAAACgAAAAHAAAAEFpckJuQl9j"
    "bG9uZS9tb2RlbHMvc3RhdGUucHk9jTEOwjAMRXefwoQFlmZgQ2JBrCxwgCoFV43UOFFs"
    "Bm5fh0h4st+33t/v/EeqnyL78tUl8wmcczeaIxPqQigalDDlN62DJQBzzanfMkxBaPzt"
    "GFPJVfFq5N4AALzWIILPJjj8+fEMaGOqB5VKQqwYekv3t5RDIrzYE2xQSwMEFAAAAAgA"
    "VV0nXR1UorWiAAAA9wAAABsAAABBaXJCbkJfY2xvbmUvbW9kZWxzL3VzZXIucHlNjj8L"
    "wkAMxfd8ilgXXdrBTXARVxfBuVx7KT3o/eGSUvz25lqwZkp+j/dejodm5tx0LjTpI2MM"
    "F6iq6kGDC4QyEs5MGX20NNUqAAw5+u3mujNM7bqj8ylmwbuSZwEA0E+GGd/qP/3w+Qqo"
    "o0kvSpmYgqDZOhYnI/YxiOkFLYlxE6MJVvVgPG3txUxeJbxpyHombVlitjsZXGZpi2ln"
    "+ss/+gJQSwMEFAAAAAgAd1InXciOWspXAAAAXgAAACEAAABBaXJCbkJfY2xvbmUvcmVx"
    "dWlyZW1lbnRzLWRldi50eHQNyj0KgDAMBtDdU3zgKg66CP5MXiTagIXYlCYKvb2uj9di"
    "55dF883J4api0CR1BuUs8SSPmkApwNnc8BjDL4b5b1QCJB6FSu2bXE8N/6nC2zr0U7eM"
    "zQdQSwMEFAAAAAgA1VEnXc5AJkVQAAAAVAAAAB4AAABBaXJCbkJfY2xvbmUvdGVzdHMv"
    "X19pbml0X18ucHlTVtQvLS7ST8rM0y+oLMnIzzPmUlJSCkktLlEoSEzOTkxPVUjLL1Io"
    "yUhVcEosTvXNT0nNUUjMS1FIy8xJ1S0uyS8CKckFcoDsvFQ9oGYuAFBLAwQUAAAACADW"
    "USddnT6OWo0BAACfAwAAHQAAAEFpckJuQl9jbG9uZS90ZXN0cy9oZWxwZXJzLnB5lZI9"
    "b9wwDIZ3/QrFHeoAB92QrUCnFB1aoC2adDYYiz7rakuCyEtwCPLfQ8kfdwmaFtVikSAf"
    "8n3ldxfbA6XtnfPbeOQ++CtVVdVXxKjxHtNRMxK/J00cEuxQE0ZIwKi7FEbNPWqIcXAt"
    "sAte6iwwGCEo5cYYEutAy41xjJ0bcIkP3nGmq4JaIjOG9reeSyJw26upYAwWBzLod86j"
    "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"
    "XKsqLrtVbuInH9DlMqrt6vSFdywEI2flaFZ30i9JO8HE/tS+LIIkh7WJ8wOec04GichQ"
    "v92nITnNDXb4KRQ6xY2CCYcXfO2iMXiXo7nBF+E7QZPmjvBKFx9ps7/1TCC3omhvwCDu"
    "4iDAh8PBdE5X0FLhChClwcn/AVBLAwQUAAAACACqXSddCC4QS+8AAACNAQAAKwAAAEFp"
    "ckJuQl9jbG9uZS90ZXN0cy90ZXN0X21vZGVscy90ZXN0X2NpdHkucHllULFOwzAQ3f0V"
    "hxkAqUoGtkqdKsZOINbKjS/1SY4d3V1QI8S/4zilQuDBst579+4939+1k3B7otSOs4ac"
    "no219h2Z+hk0IOxJZxiyx/gg4LF3U1QBlzxQCkWm6OGEwX1Q5qaMGtNzHtYJabplmoYx"
    "s1anlVQUlSZgHJHlh37VzO6Mb4XbO8Hfymp27Ap6Ux8WaJ+Tsuv0QBdKxpguOhGoDmXX"
    "43/N5u+Wp62BckrulwtyR3ItTMnjiOVKGufaVgPn6RxAguNSuaeIIKvZWnvxuQatMXZr"
    "4QW+fdsOPq2oUzySt9uydgM2uQHr+8t8A1BLAwQUAAAACADYUSddZoDeejcAAAA2AAAA"
    "NgAAAEFpckJuQl9jbG9uZS90ZXN0cy90ZXN0X21vZGVscy90ZXN0X2VuZ2luZS9fX2lu"
    "aXRfXy5weVNW1C8tLtJPyszTL6gsycjPM+ZSUlIKSS0uKVZIyy9S8Ar291NIy8xJVSgu"
    "yS9KTE/VA0pzAQBQSwMEFAAAAAgArF0nXUpIh6KIBwAAexwAAD8AAABBaXJCbkJfY2xv"
    "bmUvdGVzdHMvdGVzdF9tb2RlbHMvdGVzdF9lbmdpbmUvdGVzdF9maWxlX3N0b3JhZ2Uu"
    "cHm1Wc1uGzcQvvsp2O1FSuUN0iJAasCHNHCAtE1SxEkuhrGgdkcW411yS3JlC4aBvEBP"
    "fZwee+1LtE/SGXJ/Ja5sBY4vXlEzQ843M98MV99+87gy+vFcyMfl2i6V/OEgiqKPoMVi"
    "zYxVml8A03AhjNXcCiVnLBPmkpWgDa6BTIFxmaGIEyaJGA0cHIiiVNqyT0bJ5lmZ5qmS"
    "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"
    "uwBirdz4Ulty7OjuUhIh/jtO3EYVeLB8d+/jnh8f1j3T+uTjuhvFpfiqtNafSL4ZQRzC"
    "G148fkGbLIYnBouN6YMwmGjBR5eBghZO6MzFJ6oyWamGUlsYXFHh+7ZLJFe1AhBk4cph"
    "6JD4BniXROaMH3m2M4z3yFnwWOfugj5MrV2KQqaWgx98VErVwTDDpFDcnv+jVn99XjYK"
    "8snb7wek2vMS3EeLHeYrShjn1OIo9WcH7Azl6I0PCFzkSvxJ6brsvMr2FnsaLB+4hW/d"
    "BVPj0Vu9ydYr0D0j3ZWCg8zvH/ULUEsDBBQAAAAIAKldJ11rMjRa5AAAAIMBAAAsAAAA"
    "QWlyQm5CX2Nsb25lL3Rlc3RzL3Rlc3RfbW9kZWxzL3Rlc3Rfc3RhdGUucHllUD1PwzAQ"
    "3f0rDjMAEkoGtkqdqo6dQKzITS71SY4d3V1QI8R/x7FLEeDBw7v3ce9ub9pZuD1SbKdF"
    "fYpPxlr7ikzDAuoRntUpwph6DHcCPQ5uDirgYg8UfeYp9nBE794pcZO1xgycxqqQRoqc"
    "ximxVq86VhSVxmOYkOVnntid8CXPdk5+MYvdW5fRK/uwQrsUlV2nBzpTNMZ0wYnA6lDC"
    "7v+THv/GPGwM5JdX35+RO5Lv0hR7nDB/UcNSGqvnNJ88iHecaw8UEKS61eqr0WXVssj2"
    "0nnFr7fbwoeNbkS7yaGf5gtQSwMEFAAAAAgAqF0nXS9ACgf6AAAAsQEAACsAAABBaXJC"
    "bkJfY2xvbmUvdGVzdHMvdGVzdF9tb2RlbHMvdGVzdF91c2VyLnB5ZVA7a8MwEN71K67u"
    "0BaCM3QLZAodM/WxBsU6RweyZO7ObUzpf69kxyG0GgT6Xnef7u/Wg/D6SHHdj+pTfDZV"
    "VX0gUzuCeoR3QYYuOQwPAg5bOwQVsNEBRZ9lig6O6O0nJa6z1ZiWUzc7pB6Km7o+sU5J"
    "M6koKrXH0CPLQr9qYnvCt8ztrOCtcgo7NBm9qvcF2qWobBvd05miMaYJVgRKQpn1+F+z"
    "+jvlaWMgn7z3yxm5IbkUpuiwx3xFDePUVj2n4eRBvOVcuaWAIHPYXLvkXBad1tjOhQt8"
    "/bYtfFfYWQrVJs9cQdVn5Vdit7xbYtFDtB0uSM66AX7ML1BLAQIUAxQAAAAIAIxRJ13z"
    "GWn4RwAAAE0AAAAXAAAAAAAAAAAAAACkgQAAAABBaXJCbkJfY2xvbmUvLmdpdGlnbm9y"
    "ZVBLAQIUAxQAAAAIAIxRJ136NIcGfQAAAJ4AAAAUAAAAAAAAAAAAAACkgXwAAABBaXJC"
    "bkJfY2xvbmUvQVVUSE9SU1BLAQIUAxQAAAAIAO9dJ13z8I7vaAoAAAsYAAAWAAAAAAAA"
    "AAAAAACkgSsBAABBaXJCbkJfY2xvbmUvUkVBRE1FLm1kUEsBAhQDFAAAAAgA8F0nXW4v"
    "vx2WBgAALQ8AABoAAAAAAAAAAAAAAKSBxwsAAEFpckJuQl9jbG9uZS9TVEFSVF9IRVJF"
    "Lm1kUEsBAhQDFAAAAAgAWF0nXZIFxB8eBQAApRMAABcAAAAAAAAAAAAAAO2BlRIAAEFp"
    "ckJuQl9jbG9uZS9jb25zb2xlLnB5UEsBAhQDFAAAAAgAiVEnXQJjc+SAAAAAsAAAAB8A"
    "AAAAAAAAAAAAAO2B6BcAAEFpckJuQl9jbG9uZS9tb2RlbHMvX19pbml0X18ucHlQSwEC"
    "FAMUAAAACABXXSddY/g3iJgAAADUAAAAHgAAAAAAAAAAAAAA7YGlGAAAQWlyQm5CX2Ns"
    "b25lL21vZGVscy9hbWVuaXR5LnB5UEsBAhQDFAAAAAgAiVEnXYDsP6J/AgAAqgYAACEA"
    "AAAAAAAAAAAAAO2BeRkAAEFpckJuQl9jbG9uZS9tb2RlbHMvYmFzZV9tb2RlbC5weVBL"
    "AQIUAxQAAAAIAFZdJ13VEteEjAAAAMQAAAAbAAAAAAAAAAAAAADtgTccAABBaXJCbkJf"
    "Y2xvbmUvbW9kZWxzL2NpdHkucHlQSwECFAMUAAAACACKUSddqhR08UgAAABHAAAAJgAA"
    "AAAAAAAAAAAA7YH8HAAAQWlyQm5CX2Nsb25lL21vZGVscy9lbmdpbmUvX19pbml0X18u"
    "cHlQSwECFAMUAAAACABYXSddthwFxuwCAAB2BwAAKgAAAAAAAAAAAAAA7YGIHQAAQWly"
    "Qm5CX2Nsb25lL21vZGVscy9lbmdpbmUvZmlsZV9zdG9yYWdlLnB5UEsBAhQDFAAAAAgA"
    "VV0nXSqFcFXnAAAApAEAABwAAAAAAAAAAAAAAO2BvCAAAEFpckJuQl9jbG9uZS9tb2Rl"
    "bHMvcGxhY2UucHlQSwECFAMUAAAACABXXSdd1BZ4mJ8AAADpAAAAHQAAAAAAAAAAAAAA"
    "7YHdIQAAQWlyQm5CX2Nsb25lL21vZGVscy9yZXZpZXcucHlQSwECFAMUAAAACABWXSdd"
    "BUeGcHsAAACgAAAAHAAAAAAAAAAAAAAA7YG3IgAAQWlyQm5CX2Nsb25lL21vZGVscy9z"
    "dGF0ZS5weVBLAQIUAxQAAAAIAFVdJ10dVKK1ogAAAPcAAAAbAAAAAAAAAAAAAADtgWwj"
    "AABBaXJCbkJfY2xvbmUvbW9kZWxzL3VzZXIucHlQSwECFAMUAAAACAB3UiddyI5aylcA"
    "AABeAAAAIQAAAAAAAAAAAAAApIFHJAAAQWlyQm5CX2Nsb25lL3JlcXVpcmVtZW50cy1k"
    "ZXYudHh0UEsBAhQDFAAAAAgA1VEnXc5AJkVQAAAAVAAAAB4AAAAAAAAAAAAAAO2B3SQA"
    "AEFpckJuQl9jbG9uZS90ZXN0cy9fX2luaXRfXy5weVBLAQIUAxQAAAAIANZRJ12dPo5a"
    "jQEAAJ8DAAAdAAAAAAAAAAAAAADtgWklAABBaXJCbkJfY2xvbmUvdGVzdHMvaGVscGVy"
    "cy5weVBLAQIUAxQAAAAIAKhdJ10eYQeadwUAAN0UAAAhAAAAAAAAAAAAAADtgTEnAABB"
    "aXJCbkJfY2xvbmUvdGVzdHMvbW9kZWxfY2FzZXMucHlQSwECFAMUAAAACADuXSdd903e"
    "gHMKAAC0KAAAIgAAAAAAAAAAAAAA7YHnLAAAQWlyQm5CX2Nsb25lL3Rlc3RzL3Rlc3Rf"
    "Y29uc29sZS5weVBLAQIUAxQAAAAIAO9dJ1086PrqUwcAAOoYAAAmAAAAAAAAAAAAAADt"
    "gZo3AABBaXJCbkJfY2xvbmUvdGVzdHMvdGVzdF9pbnRlZ3JhdGlvbi5weVBLAQIUAxQA"
    "AAAIANdRJ132RlDJRgAAAEYAAAAqAAAAAAAAAAAAAADtgTE/AABBaXJCbkJfY2xvbmUv"
    "dGVzdHMvdGVzdF9tb2RlbHMvX19pbml0X18ucHlQSwECFAMUAAAACACqXSddL0YNSOsA"
    "AACPAQAALgAAAAAAAAAAAAAA7YG/PwAAQWlyQm5CX2Nsb25lL3Rlc3RzL3Rlc3RfbW9k"
    "ZWxzL3Rlc3RfYW1lbml0eS5weVBLAQIUAxQAAAAIAHZSJ135z6emhAgAACkeAAAxAAAA"
    "AAAAAAAAAADtgfZAAABBaXJCbkJfY2xvbmUvdGVzdHMvdGVzdF9tb2RlbHMvdGVzdF9i"
    "YXNlX21vZGVsLnB5UEsBAhQDFAAAAAgAql0nXQguEEvvAAAAjQEAACsAAAAAAAAAAAAA"
    "AO2ByUkAAEFpckJuQl9jbG9uZS90ZXN0cy90ZXN0X21vZGVscy90ZXN0X2NpdHkucHlQ"
    "SwECFAMUAAAACADYUSddZoDeejcAAAA2AAAANgAAAAAAAAAAAAAA7YEBSwAAQWlyQm5C"
    "X2Nsb25lL3Rlc3RzL3Rlc3RfbW9kZWxzL3Rlc3RfZW5naW5lL19faW5pdF9fLnB5UEsB"
    "AhQDFAAAAAgArF0nXUpIh6KIBwAAexwAAD8AAAAAAAAAAAAAAO2BjEsAAEFpckJuQl9j"
    "bG9uZS90ZXN0cy90ZXN0X21vZGVscy90ZXN0X2VuZ2luZS90ZXN0X2ZpbGVfc3RvcmFn"
    "ZS5weVBLAQIUAxQAAAAIAKldJ13Yhd0S9QEAAFQEAAAsAAAAAAAAAAAAAADtgXFTAABB"
    "aXJCbkJfY2xvbmUvdGVzdHMvdGVzdF9tb2RlbHMvdGVzdF9wbGFjZS5weVBLAQIUAxQA"
    "AAAIAKtdJ13k0pIJ9gAAAKgBAAAtAAAAAAAAAAAAAADtgbBVAABBaXJCbkJfY2xvbmUv"
    "dGVzdHMvdGVzdF9tb2RlbHMvdGVzdF9yZXZpZXcucHlQSwECFAMUAAAACACpXSddazI0"
    "WuQAAACDAQAALAAAAAAAAAAAAAAA7YHxVgAAQWlyQm5CX2Nsb25lL3Rlc3RzL3Rlc3Rf"
    "bW9kZWxzL3Rlc3Rfc3RhdGUucHlQSwECFAMUAAAACACoXSddL0AKB/oAAACxAQAAKwAA"
    "AAAAAAAAAAAA7YEfWAAAQWlyQm5CX2Nsb25lL3Rlc3RzL3Rlc3RfbW9kZWxzL3Rlc3Rf"
    "dXNlci5weVBLBQYAAAAAHwAfANsJAABiWQAAAAA="
)


def project_files(authors):
    """Decode the bundled project and optionally personalize AUTHORS."""
    result = {}
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(PAYLOAD))) as archive:
        for member in archive.infolist():
            parts = PurePosixPath(member.filename).parts
            if (len(parts) < 2 or parts[0] != "AirBnB_clone"
                    or ".." in parts or member.is_dir()):
                raise ValueError("Unexpected archive path: " + member.filename)
            relative = Path(*parts[1:])
            result[relative] = archive.read(member)
    if authors:
        content = "# Contributors to this repository, one person per line.\n"
        content += "\n".join(authors) + "\n"
        result[Path("AUTHORS")] = content.encode("utf-8")
    return result


def conflicts_in(target, contents, update=False):
    """Find incompatible files and path components before writing."""
    conflicts = set()
    for relative, data in contents.items():
        destination = target / relative
        if destination.is_symlink():
            conflicts.add(str(relative))
        elif destination.exists():
            if not destination.is_file():
                conflicts.add(str(relative))
            elif not update and destination.read_bytes() != data:
                conflicts.add(str(relative))
        for parent in destination.parents:
            if parent == target.parent:
                break
            if (parent.is_symlink()
                    or (parent.exists() and not parent.is_dir())):
                conflicts.add(str(parent))
    return sorted(conflicts)


def backup_changes(target, contents):
    """Back up changed files before the update writes anything."""
    changed = [relative for relative, data in contents.items()
               if (target / relative).is_file()
               and (target / relative).read_bytes() != data]
    if not changed:
        return None
    prefix = "{}_backup_{}_".format(
        target.name, datetime.now().strftime("%Y%m%dT%H%M%S"))
    descriptor, filename = tempfile.mkstemp(
        prefix=prefix, suffix=".zip", dir=str(target.parent))
    os.close(descriptor)
    backup = Path(filename)
    try:
        with zipfile.ZipFile(backup, "w", zipfile.ZIP_DEFLATED) as archive:
            for relative in changed:
                archive.write(target / relative, str(relative))
            metadata = {
                "project": str(target),
                "replaced_files": [str(relative) for relative in changed],
                "new_files": [str(relative) for relative in contents
                              if not (target / relative).exists()],
            }
            archive.writestr("RESTORE_INFO.json",
                             json.dumps(metadata, indent=2))
    except Exception:
        backup.unlink()
        raise
    return backup


def write_project_file(destination, data):
    """Write a new file exclusively, or replace an existing file atomically."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        with destination.open("xb") as stream:
            stream.write(data)
        if destination.suffix == ".py":
            destination.chmod(0o755)
        return
    mode = destination.stat().st_mode & 0o777
    descriptor, filename = tempfile.mkstemp(
        prefix=".airbnb-update-", dir=str(destination.parent))
    temporary = Path(filename)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        temporary.chmod(0o755 if destination.suffix == ".py" else mode)
        os.replace(str(temporary), str(destination))
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv=None):
    """Create the project or apply a backed-up update to an existing one."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="AirBnB_clone",
                        help="project directory (default: AirBnB_clone)")
    parser.add_argument("--author", action="append",
                        help="name and email; repeat for teammates")
    parser.add_argument("--update", action="store_true",
                        help="update an existing project with a backup")
    options = parser.parse_args(argv)
    authors = options.author
    if authors:
        authors = [author.strip() for author in authors]
        if any(not author or "\n" in author or "\r" in author
               for author in authors):
            parser.error("Each --author must be one nonempty line.")
    target = Path(options.target).expanduser().resolve()
    contents = project_files(authors)
    try:
        base_path = target / "models" / "base_model.py"
        if options.update and not base_path.is_file():
            parser.error("Use your existing project folder as --target.")
        if options.update:
            if not authors and (target / "AUTHORS").is_file():
                contents.pop(Path("AUTHORS"), None)
            if (target / ".gitignore").is_file():
                contents.pop(Path(".gitignore"), None)
        conflicts = conflicts_in(target, contents, update=options.update)
        if conflicts:
            print("No files were changed. Conflicting paths:", file=sys.stderr)
            for path in conflicts:
                print("  " + path, file=sys.stderr)
            print("Use --update for file changes, or choose a new folder.",
                  file=sys.stderr)
            return 1
        target.mkdir(parents=True, exist_ok=True)
        backup = backup_changes(target, contents) if options.update else None
        if backup is not None:
            print("Backup of replaced files: {}".format(backup), flush=True)
        created = updated = kept = 0
        for relative, data in contents.items():
            destination = target / relative
            if destination.exists():
                if destination.read_bytes() == data:
                    kept += 1
                    continue
                if not options.update:
                    raise FileExistsError(str(destination))
                write_project_file(destination, data)
                updated += 1
            else:
                write_project_file(destination, data)
                created += 1
    except OSError as error:
        print("Setup could not finish: {}".format(error), file=sys.stderr)
        return 1
    print("Project ready: {}".format(target))
    print("Created {}; updated {}; kept {} identical files.".format(
        created, updated, kept))
    if not authors and not options.update:
        print("Before submission, replace the example name/email in AUTHORS.")
    print("Open that folder and run: python3 -m unittest discover tests")
    print("Start the interpreter with: python3 console.py")
    print("See START_HERE.md to commit all files to GitHub together.")
    return 0


if __name__ == "__main__":
    sys.exit(main())