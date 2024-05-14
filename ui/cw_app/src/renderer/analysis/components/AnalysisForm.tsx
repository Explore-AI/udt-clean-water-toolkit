import { useForm, SubmitHandler } from "react-hook-form"

type Inputs = {
  example: string
  exampleRequired: string
}

export default function AnalysisForm(props) {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<Inputs>()
  const { onSubmit } = props


  console.log(watch("example")) // watch input value by passing the name of it

  return (
    /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input defaultValue="test" {...register("example")} />
      </div>
      <div>
        <input {...register("exampleRequired", { required: true })} />
      </div>
        {errors.exampleRequired && <span>This field is required</span>}

      <div>
        <input type="submit" />
      </div>
    </form>
  )
}
